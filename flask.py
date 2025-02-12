from flask import Flask, request, jsonify
import redis
from rq import Queue, Worker
from subprocess import Popen, PIPE
import logging
import time
from threading import Thread

# Set up Flask app
app = Flask(__name__)

# Set up Redis connection
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to clone a Git repository
def clone_repository(git_url, branch_name):
    logging.info(f"Started cloning repository: {git_url} for branch: {branch_name}")

    try:
        process = Popen(['git', 'clone', '-b', branch_name, git_url], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            logging.error(f"Error cloning repository: {stderr.decode()}")
            return f"Error: {stderr.decode()}"
        
        logging.info(f"Cloning completed successfully for {branch_name} branch")
        return f"Success: {stdout.decode()}"
    
    except Exception as e:
        logging.error(f"Error processing git clone: {str(e)}")
        return f"Error: {str(e)}"

# Function to process jobs from a queue
def process_jobs(queue):
    while True:
        job = queue.get()
        if job:
            logging.info(f"Processing job: {job.id}")
            job.result = clone_repository(*job.args)
            job.save()  # Save the job result after completion

# Webhook endpoint to receive GitHub webhook events
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info(f"Received webhook data: {data}")

    # Extract branch name and git URL from the webhook payload
    branch_name = data.get('ref', '').split('/')[-1]  # 'ref' contains the branch name (e.g., 'refs/heads/main')
    git_url = data.get('repository', {}).get('clone_url', '')

    if not git_url:
        return jsonify({'error': 'No git URL found in webhook data'}), 400

    if not branch_name:
        return jsonify({'error': 'No branch name found in webhook data'}), 400

    # Create a separate queue for each branch (by branch name)
    queue = Queue(branch_name, connection=redis_conn)  # Use branch name as queue name

    # Enqueue the job to the Redis queue
    job = queue.enqueue(clone_repository, git_url, branch_name, result_ttl=3600, retries=3, retry_interval=30)

    logging.info(f"Job {job.id} added to queue for branch {branch_name}")

    return jsonify({'message': f'Webhook received and job added to queue for branch {branch_name}', 'job_id': job.id}), 200

# Start a background thread to process the jobs
def start_worker():
    while True:
        # This will ensure that jobs are processed for each branch
        for branch in ['main', 'dev']:  # Add more branches as needed
            queue = Queue(branch, connection=redis_conn)
            process_jobs(queue)
        time.sleep(10)

# Start worker thread on app startup
@app.before_first_request
def before_first_request():
    worker_thread = Thread(target=start_worker)
    worker_thread.daemon = True
    worker_thread.start()

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
