import os
import subprocess
import shutil
import redis
import threading
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connect to Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Directory to clone repositories into
CLONE_DIR = "/path/to/clone/directory"  # Replace with the actual path where you want to clone repos

# Directory to copy the cloned repositories into
DESTINATION_DIR = "/path/to/destination/directory"  # Replace with the destination path

# Dictionary to hold locks for each branch
branch_locks = {}

def process_task(task_data, branch):
    repo_url = task_data.get("repo_url")
    if not repo_url:
        print("No repository URL provided")
        return
    
    # Create a subdirectory for this repository clone (to avoid collisions)
    repo_name = repo_url.split("/")[-1].replace(".git", "")  # Extract repo name from URL
    clone_path = os.path.join(CLONE_DIR, repo_name)
    destination_path = os.path.join(DESTINATION_DIR, repo_name)

    try:
        # If the repository is not already cloned, clone it
        if not os.path.exists(clone_path):
            print(f"Cloning repository {repo_url} to {clone_path}")
            subprocess.run(["git", "clone", repo_url, clone_path], check=True, capture_output=True, text=True)
            print(f"Repository cloned successfully to {clone_path}")
        
        # Fetch the latest changes from the remote repository
        subprocess.run(["git", "fetch"], cwd=clone_path, check=True, capture_output=True, text=True)
        print("Fetched the latest changes.")

        # Run git pull to pull the latest changes
        subprocess.run(["git", "pull"], cwd=clone_path, check=True, capture_output=True, text=True)
        print("Git pull completed.")

        # Get the list of all files in the cloned repository
        files_to_copy = get_files_to_copy(clone_path)

        if files_to_copy:
            print(f"Files to copy: {files_to_copy}")
            
            # Copy the files to the destination directory
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

            for file in files_to_copy:
                source_file = os.path.join(clone_path, file)
                dest_file = os.path.join(destination_path, file)
                dest_dir = os.path.dirname(dest_file)
                
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                shutil.copy2(source_file, dest_file)
                print(f"Copied {file} to {dest_file}")
        else:
            print("No files to copy.")
    
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def get_files_to_copy(clone_path):
    """
    Get the list of all files in the repository.
    This is based on the assumption that after pulling, all the files will be copied.
    """
    try:
        # Use `git ls-files` to get a list of all tracked files in the repository
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=clone_path,
            check=True,
            capture_output=True,
            text=True
        )
        # Return the list of files
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error getting files to copy: {e.stderr}")
        return []

@app.route('/api', methods=['POST'])
def add_task():
    # Get the repository URL and branch from the request
    data = request.json
    repo_url = data.get("repo_url")
    branch = data.get("branch")
    
    if not repo_url or not branch:
        return jsonify({"status": "error", "message": "Repository URL and branch are required"}), 400

    # Ensure that a lock exists for this branch
    if branch not in branch_locks:
        branch_locks[branch] = threading.Lock()

    # Add the task to the Redis queue specific to the branch
    queue_name = f"task_queue_{branch}"
    redis_client.lpush(queue_name, json.dumps(data))
    
    return jsonify({"status": "Request added to the queue", "repo_url": repo_url, "branch": branch})

@app.route('/status', methods=['GET'])
def queue_status():
    # Get the number of tasks currently in the queue for each branch
    branch_queue_lengths = {}
    for branch in branch_locks.keys():
        queue_name = f"task_queue_{branch}"
        branch_queue_lengths[branch] = redis_client.llen(queue_name)
    
    return jsonify({"status": "Queue status", "tasks_in_queue": branch_queue_lengths})

def worker(branch):
    while True:
        # Wait for a task from the specific branch's queue
        queue_name = f"task_queue_{branch}"
        task_data = redis_client.rpop(queue_name)
        if task_data:
            task_data = json.loads(task_data)
            # Acquire lock to ensure only one task is processed for the given branch
            with branch_locks[branch]:
                process_task(task_data, branch)

if __name__ == '__main__':
    # Example: Start a worker for each branch you expect to process
    initial_branches = ["main", "develop"]  # You can add any branches you want here
    for branch in initial_branches:
        worker_thread = threading.Thread(target=worker, args=(branch,))
        worker_thread.daemon = True
        worker_thread.start()

    # Start the Flask application
    app.run(debug=True)
