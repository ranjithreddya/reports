from flask import Flask, request, jsonify
import hmac
import hashlib
import json
import boto3
import requests
from datetime import datetime

app = Flask(__name__)

# Bitbucket Webhook Secret (to validate the webhook authenticity)
BITBUCKET_SECRET = 'your_bitbucket_webhook_secret'

# AWS S3 Configuration
AWS_ACCESS_KEY = 'your_aws_access_key'
AWS_SECRET_KEY = 'your_aws_secret_key'
S3_BUCKET_NAME = 'your_s3_bucket_name'
REGION_NAME = 'your_aws_region'

# Create a boto3 S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY, region_name=REGION_NAME)

# Verify Bitbucket Webhook Signature
def verify_bitbucket_signature(data, signature):
    computed_signature = hmac.new(BITBUCKET_SECRET.encode(), msg=data.encode(), digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, signature)

# Handle Bitbucket Push Webhook
@app.route('/webhook/bitbucket', methods=['POST'])
def bitbucket_webhook():
    # Get the signature from Bitbucket's request headers
    signature = request.headers.get('X-Event-Key')
    
    if not signature:
        return jsonify({"error": "Signature missing"}), 400
    
    # Validate signature
    if not verify_bitbucket_signature(request.data.decode(), signature):
        return jsonify({"error": "Invalid signature"}), 400

    payload = request.json
    event_key = payload.get('event_key')

    if event_key == 'repo:push':
        # Example: Push event, extract repo info
        repository = payload['repository']['name']
        commits = payload['push']['changes'][0]['commits']

        # Log commit details
        for commit in commits:
            print(f"Commit ID: {commit['hash']}")
            print(f"Author: {commit['author']['raw']}")
            print(f"Message: {commit['message']}")

        # Optional: Trigger deployment, code sync, etc.
        trigger_deployment(repository)

    return jsonify({"status": "success"}), 200

# Trigger Deployment (dummy function to simulate deployment)
def trigger_deployment(repository):
    # Example: Clone the repository, pull latest changes, etc.
    print(f"Deployment triggered for repository: {repository}")

    # You can extend this logic to interact with servers or CI/CD systems.

# Handle S3 File Upload via Webhook (For example, from Bitbucket)
@app.route('/webhook/s3', methods=['POST'])
def s3_upload():
    try:
        # Assume the payload contains information on what file to upload to S3
        data = request.json
        file_name = data.get('file_name')
        file_content = data.get('file_content')  # Example: Base64 or direct content

        if not file_name or not file_content:
            return jsonify({"error": "File name and content are required"}), 400

        # Upload to S3
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_name,
            Body=file_content
        )
        return jsonify({"status": "File uploaded successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to upload file to S3"}), 500

# Example endpoint to simulate Bitbucket push (for testing)
@app.route('/test/bitbucket', methods=['POST'])
def test_bitbucket():
    test_data = {
        "event_key": "repo:push",
        "repository": {"name": "my_repo"},
        "push": {"changes": [{"commits": [{"hash": "abcd1234", "author": {"raw": "John Doe"},"message": "Fix issue"}]}]}
    }
    response = app.test_client().post('/webhook/bitbucket', json=test_data)
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
