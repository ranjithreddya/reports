# project/
# ├── app.py              # Flask app
# ├── celery_app.py       # Celery app setup
# ├── tasks.py            # Celery task
# ├── requirements.txt    # Dependencies


# # celery.py
# from celery import Celery

# celery_app = Celery(
#     'myapp',
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/0'
# )

# # Dynamically route tasks based on branch name
# celery_app.conf.task_routes = {
#     'tasks.process_payload': lambda args, kwargs, **_: {
#         'queue': f"{kwargs.get('branch', 'default')}_queue"
#     }
# }


# # tasks.py
# from celery_app import celery_app
# import time
# import random

# @celery_app.task(bind=True)
# def process_payload(self, payload, branch):
#     print(f"[{branch}] START: {payload}")

#     # Simulate variable processing time (e.g. 1–30 mins)
#     simulated_minutes = random.randint(1, 3)  # For testing; change to (1, 30) in production
#     time.sleep(simulated_minutes * 60)

#     print(f"[{branch}] DONE: {payload}")
#     return {"branch": branch, "duration_minutes": simulated_minutes}

# # app.py
# from flask import Flask, request, jsonify
# from tasks import process_payload

# app = Flask(__name__)

# @app.route('/submit', methods=['POST'])
# def submit():
#     data = request.get_json()
#     branch = data.get('branch')

#     if not branch:
#         return jsonify({"error": "Missing 'branch' in payload"}), 400

#     task = process_payload.apply_async(
#         kwargs={'payload': data, 'branch': branch}
#     )

#     return jsonify({
#         "task_id": task.id,
#         "branch": branch,
#         "status": "submitted"
#     })

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)




# celery -A celery_app worker -Q asic_queue --concurrency=1 --loglevel=info
# celery -A celery_app worker -Q noa_queue --concurrency=1 --loglevel=info


# celery -A celery_app worker -Q asic_queue --concurrency=1 --loglevel=info & \
# celery -A celery_app worker -Q noa_queue --concurrency=1 --loglevel=info & \
# celery -A celery_app worker -Q mas_queue --concurrency=4 --loglevel=info


# celery -A celery_app worker -Q asic_queue,noa_queue --concurrency=1 --loglevel=info







##############################################################################################################


deploy_project/
├── app.py
├── celery_config.py
├── tasks.py
├── wsgi.py
├── requirements.txt

###########################

Flask
celery
redis
GitPython


############################

celery_config.py

from celery import Celery

celery_app = Celery(
    'deploy_project',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True
)


################################

tasks.py
from celery_config import celery_app
from git import Repo
import os
import shutil
from celery import group

# Set these paths accordingly
REPO_PATH = "/path/to/your/git/repo"      # <- Change this
TARGET_DIR = "/path/to/target/location"   # <- Change this

@celery_app.task
def prepare_code_task(branch):
    repo = Repo(REPO_PATH)
    origin = repo.remotes.origin

    # Step 1: Fetch
    origin.fetch()

    # Step 2: Diff
    local_commit = repo.head.commit
    remote_commit = repo.commit(f'origin/{branch}')
    diff_files = [item.a_path for item in local_commit.diff(remote_commit)]

    # Step 3: Pull
    origin.pull(branch)

    return {
        'branch': branch,
        'files': diff_files
    }

@celery_app.task
def copy_file(file_path):
    source = os.path.join(REPO_PATH, file_path)
    dest = os.path.join(TARGET_DIR, file_path)

    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(source, dest)

@celery_app.task
def copy_files_task(data):
    files = data.get('files', [])
    if not files:
        return {"branch": data['branch'], "status": "no files to copy"}

    jobs = group(copy_file.s(file) for file in files)
    jobs.apply_async().get()  # wait for all copies to complete

    return {"branch": data['branch'], "status": "copied", "files": len(files)}



##########################################################

apps.py

from flask import Flask, request, jsonify
from tasks import prepare_code_task, copy_files_task
from celery import chain

app = Flask(__name__)

@app.route('/deploy', methods=['POST'])
def deploy():
    data = request.get_json()
    branch = data.get("branch")
    if not branch:
        return jsonify({"error": "branch is required"}), 400

    # Chain: fetch → diff → pull → copy files
    task_chain = chain(
        prepare_code_task.s(branch),
        copy_files_task.s()
    )

    # Send to queue named by branch
    task_chain.apply_async(queue=f"queue_{branch}")

    return jsonify({"status": "queued", "branch": branch})




#############################################################

`
celery -A celery_config worker -Q queue_asic -n worker_asic@%h --concurrency=1


redis-cli
LRANGE queue:queue_asic 0 -1


