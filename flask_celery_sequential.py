project/
├── app.py              # Flask app
├── celery_app.py       # Celery app setup
├── tasks.py            # Celery task
├── requirements.txt    # Dependencies


# celery.py
from celery import Celery

celery_app = Celery(
    'myapp',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Dynamically route tasks based on branch name
celery_app.conf.task_routes = {
    'tasks.process_payload': lambda args, kwargs, **_: {
        'queue': f"{kwargs.get('branch', 'default')}_queue"
    }
}


# tasks.py
from celery_app import celery_app
import time
import random

@celery_app.task(bind=True)
def process_payload(self, payload, branch):
    print(f"[{branch}] START: {payload}")

    # Simulate variable processing time (e.g. 1–30 mins)
    simulated_minutes = random.randint(1, 3)  # For testing; change to (1, 30) in production
    time.sleep(simulated_minutes * 60)

    print(f"[{branch}] DONE: {payload}")
    return {"branch": branch, "duration_minutes": simulated_minutes}

# app.py
from flask import Flask, request, jsonify
from tasks import process_payload

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    branch = data.get('branch')

    if not branch:
        return jsonify({"error": "Missing 'branch' in payload"}), 400

    task = process_payload.apply_async(
        kwargs={'payload': data, 'branch': branch}
    )

    return jsonify({
        "task_id": task.id,
        "branch": branch,
        "status": "submitted"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)




celery -A celery_app worker -Q asic_queue --concurrency=1 --loglevel=info
celery -A celery_app worker -Q noa_queue --concurrency=1 --loglevel=info


celery -A celery_app worker -Q asic_queue --concurrency=1 --loglevel=info & \
celery -A celery_app worker -Q noa_queue --concurrency=1 --loglevel=info & \
celery -A celery_app worker -Q mas_queue --concurrency=4 --loglevel=info


celery -A celery_app worker -Q asic_queue,noa_queue --concurrency=1 --loglevel=info
