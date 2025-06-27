#app.py:
from flask import Flask, request, jsonify
from celery import chain
from tasks import prepare_code_task, copy_files_task

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    branch = data.get("branch")
    if not branch:
        return jsonify({"error": "branch is required"}), 400

    task_chain = chain(
        prepare_code_task.s(branch),
        copy_files_task.s()
    )
    task_chain.apply_async(queue=f"queue_{branch}")

    return jsonify({"status": "queued", "branch": branch})



if __name__ == "__main__":
    app.run(debug=True)


#tasks.py
import os
import shutil
from celery import group, states
from celery.exceptions import Ignore
from celery_config import celery_app
import redis
import json

REPO_PATH = "/tmp/source_repo"         # Adjust to your repo path
TARGET_DIR = "/tmp/deployment_target"  # Adjust to your deploy path

redis_client = redis.StrictRedis(host='localhost', port=6379, db=2, decode_responses=True)

def failed_files_key(branch):
    return f"failed_files:{branch}"

def load_failed_files(branch):
    data = redis_client.get(failed_files_key(branch))
    return json.loads(data) if data else []

def save_failed_files(branch, files):
    redis_client.set(failed_files_key(branch), json.dumps(files))

@celery_app.task(name="prepare_code_task")
def prepare_code_task(branch):
    # Simulate git fetch/diff/pull
    changed_files = ['main.py', 'lib/utils.py']
    deleted_files = ['old_config.yaml']
    return {"branch": branch, "changed_files": changed_files, "deleted_files": deleted_files}

@celery_app.task(bind=True, name="copy_file")
def copy_file(self, file_path, branch):
    src = os.path.join(REPO_PATH, file_path)
    dest = os.path.join(TARGET_DIR, file_path)

    try:
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
    except Exception as e:
        self.update_state(state=states.FAILURE, meta=str(e))
        failed = load_failed_files(branch)
        if file_path not in failed:
            failed.append(file_path)
            save_failed_files(branch, failed)
        raise Ignore()

    # Remove from failed list on success
    failed = load_failed_files(branch)
    if file_path in failed:
        failed.remove(file_path)
        save_failed_files(branch, failed)

@celery_app.task(name="delete_file")
def delete_file(file_path):
    target = os.path.join(TARGET_DIR, file_path)
    try:
        if os.path.exists(target):
            os.remove(target)
    except Exception as e:
        raise e

@celery_app.task(name="copy_files_task")
def copy_files_task(data):
    branch = data.get('branch')
    changed_files = data.get('changed_files', [])
    deleted_files = data.get('deleted_files', [])

    results = {"branch": branch, "copied": 0, "deleted": 0}

    # Copy changed files
    if changed_files:
        failed_files = load_failed_files(branch)
        files_to_copy = failed_files + [f for f in changed_files if f not in failed_files]
        copy_jobs = group(copy_file.s(file, branch) for file in files_to_copy)
        copy_jobs.apply_async().get()
        results["copied"] = len(files_to_copy)

    # Delete files
    if deleted_files:
        delete_jobs = group(delete_file.s(file) for file in deleted_files)
        delete_jobs.apply_async().get()
        results["deleted"] = len(deleted_files)

    return results


#celery_config.py
from celery import Celery

celery_app = Celery(
    "myapp",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

# Register tasks explicitly
import tasks

###########################################################
celery -A celery_config.celery_app worker --loglevel=info -Q queue_main --concurrency=4

celery -A celery_config.celery_app worker --loglevel=info -Q queue_main
python app.py






########################
from celery import Celery

celery_app = Celery(
    "deploy_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

celery_app.conf.task_routes = {
    "copy_file": {"queue": "default"},
    "delete_file": {"queue": "default"},
    "prepare_code_task": {"queue": "default"},
    "dispatch_parallel_tasks": {"queue": "default"},
}


from celery import chord, group
from celery_config import celery_app
import os
import shutil
import redis
import json

REPO_PATH = "/tmp/source_repo"
TARGET_DIR = "/tmp/deployment_target"

redis_client = redis.StrictRedis(host="localhost", port=6379, db=2, decode_responses=True)

@celery_app.task(name="prepare_code_task")
def prepare_code_task(branch):
    changed_files = ["main.py", "lib/utils.py"]
    deleted_files = ["old_config.yaml"]
    redis_client.set(f"deploy:{branch}", json.dumps({
        "changed_files": changed_files,
        "deleted_files": deleted_files
    }))
    return {"changed_files": changed_files, "deleted_files": deleted_files}

@celery_app.task(name="copy_file")
def copy_file(file_path, branch):
    try:
        src = os.path.join(REPO_PATH, file_path)
        dest = os.path.join(TARGET_DIR, file_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        return {"status": "copied", "file": file_path}
    except Exception as e:
        return {"status": "error", "file": file_path, "error": str(e)}

@celery_app.task(name="delete_file")
def delete_file(file_path):
    try:
        target = os.path.join(TARGET_DIR, file_path)
        if os.path.exists(target):
            os.remove(target)
        return {"status": "deleted", "file": file_path}
    except Exception as e:
        return {"status": "error", "file": file_path, "error": str(e)}

@celery_app.task(name="dispatch_parallel_tasks")
def dispatch_parallel_tasks(result_from_prepare, branch):
    changed_files = result_from_prepare.get("changed_files", [])
    deleted_files = result_from_prepare.get("deleted_files", [])

    tasks = [
        copy_file.s(file, branch) for file in changed_files
    ] + [
        delete_file.s(file) for file in deleted_files
    ]

    return chord(tasks)(finalize_deploy.s(branch))

@celery_app.task(name="finalize_deploy")
def finalize_deploy(results, branch):
    copied = [r for r in results if r["status"] == "copied"]
    deleted = [r for r in results if r["status"] == "deleted"]
    failed = [r for r in results if r["status"] == "error"]

    summary = {
        "branch": branch,
        "copied": [f["file"] for f in copied],
        "deleted": [f["file"] for f in deleted],
        "failed": failed
    }

    print(f"[FINALIZE] Deployment Summary for {branch}:\n{json.dumps(summary, indent=2)}")
    return summary


from flask import Flask, request, jsonify
from celery import chain
from tasks import prepare_code_task, dispatch_parallel_tasks

app = Flask(__name__)

@app.route("/deploy", methods=["POST"])
def deploy():
    data = request.get_json()
    branch = data.get("branch")
    if not branch:
        return jsonify({"error": "branch is required"}), 400

    chain(
        prepare_code_task.s(branch),
        dispatch_parallel_tasks.s(branch)
    ).apply_async(queue=f"queue_{branch}")

    return jsonify({"status": "queued", "branch": branch})

if __name__ == "__main__":
    app.run(debug=True)



#!/bin/bash

# Start worker for "main" branch
celery -A celery_config.celery_app worker -Q queue_main --concurrency=1 --loglevel=info
