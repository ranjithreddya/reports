import os
import shutil
import redis
import threading
import json
import time
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

def run_git_command(command, cwd):
    """
    Run a git command using os.system.
    This function returns the output of the command.
    """
    command_str = " ".join(command)
    print(f"Running command: {command_str} in {cwd}")
    return os.system(command_str)

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
        # Add a sleep before the first request runs
        if not os.path.exists(clone_path):
            print("Sleeping before first request processing...")
            time.sleep(120)  # Sleep for 120 seconds (2 minutes)

        # If the repository is not already cloned, clone it
        if not os.path.exists(clone_path):
            print(f"Cloning repository {repo_url} to {clone_path}")
            run_git_command(["git", "clone", repo_url, clone_path], clone_path)
            print(f"Repository cloned successfully to {clone_path}")
        
        # Fetch the latest changes from the remote repository
        run_git_command(["git", "fetch"], clone_path)
        print("Fetched the latest changes.")

        # Run git pull to pull the latest changes
        run_git_command(["git", "pull"], clone_path)
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
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

def get_files_to_copy(clone_path):
    """
    Get the list of all files in the repository.
    This is based on the assumption that after pulling, all the files will be copied.
    """
    try:
        # Use `git ls-files` to get a list of all tracked files in the repository
        result = os.popen(f"git ls-files").read()
        # Return the list of files
        return result.splitlines()
    except Exception as e:
        print(f"Error getting files to copy: {str(e)}")
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
    
    # Start worker dynamically for this branch if it is not already running
    start_worker_if_not_running(branch)
    
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

def start_worker_if_not_running(branch):
    """
    Start a worker for the branch if it is not already running.
    This function checks if the worker thread for the branch is already active.
    """
    if branch not in branch_locks or not any(thread.name == branch for thread in threading.enumerate()):
        worker_thread = threading.Thread(target=worker, args=(branch,))
        worker_thread.daemon = True  # Daemonize the thread (it will exit when the program exits)
        worker_thread.name = branch  # Name the thread with the branch name
        worker_thread.start()
        print(f"Worker started for branch: {branch}")
    else:
        print(f"Worker already running for branch: {branch}")

if __name__ == '__main__':
    # Start the Flask application on a custom port (e.g., 8080)
    app.run(debug=True, host="0.0.0.0", port=8080)










import subprocess

def get_files_to_copy(remote_branch='origin/main'):
    """
    Get the list of files that differ between the local repository and the remote repository.
    This compares your current branch with the given remote branch.
    """
    try:
        # Fetch the latest updates from the remote repository
        subprocess.run(["git", "fetch", "origin"], check=True)

        # Get the list of files that have changed between the local and remote branch
        result = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD", remote_branch], 
            stderr=subprocess.STDOUT
        ).decode('utf-8')

        # Return the list of file names that have changed
        return result.splitlines()
    
    except subprocess.CalledProcessError as e:
        print(f"Error getting file list: {e.output.decode()}")
        return []

# Example usage
files_to_copy = get_files_to_copy('origin/main')
print("Files to copy:")
for file in files_to_copy:
    print(file)



The 12-character replacement, which includes the date and an incremental value (200000), is essential for guaranteeing that each request is assigned a unique identifier. This approach prevents duplication, which is crucial for tracking individual transactions or processes accurately, especially when multiple requests are made on the same day. Ensuring unique identifiers helps maintain data integrity and avoids potential conflicts or errors in the system.
