import subprocess

def sync_local_to_s3(local_directory, s3_bucket):
    # Construct the AWS S3 sync command
    command = [
        "aws", "s3", "sync", local_directory, s3_bucket
    ]
    
    # Execute the command
    try:
        subprocess.run(command, check=True)
        print(f"Sync completed from {local_directory} to {s3_bucket}")
    except subprocess.CalledProcessError as e:
        print(f"Error during sync: {e}")

# Usage
local_directory = "/path/to/local/folder"
s3_bucket = "s3://your-bucket-name"
sync_local_to_s3(local_directory, s3_bucket)



import boto3
import os

def sync_local_to_s3(local_directory, s3_bucket):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    
    # Walk through the local directory
    for root, dirs, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_directory)
            s3_file_path = os.path.join(s3_bucket, relative_path)

            # Upload the file
            s3_client.upload_file(local_file_path, s3_bucket, relative_path)
            print(f"Uploaded: {local_file_path} -> {s3_file_path}")

# Usage
local_directory = "/path/to/local/folder"
s3_bucket = "your-bucket-name"
sync_local_to_s3(local_directory, s3_bucket)



from boto3.s3.transfer import S3Transfer
from boto3.s3.transfer import TransferConfig

# You can configure transfer to use a custom chunk size or number of threads
config = TransferConfig(
    multipart_threshold=1024 * 25,  # The size (in bytes) to trigger multipart upload
    max_concurrency=10,  # Number of parallel threads to use for uploading
)

# Set up the transfer with a custom config
transfer = S3Transfer(s3_client, config)

# Upload the file with progress
transfer.upload_file('path/to/local/file', 'your-bucket-name', 'file/on/s3', extra_args=None)
