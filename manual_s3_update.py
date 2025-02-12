import boto3
import os

# Initialize the S3 client
s3 = boto3.client('s3')

# List of data to process
data = [
    {
        "input_manual_upload": {
            "filename": "/apps/DPO/test.csv",
            "s3_path": "test/DPO/test.csv"
        },
        "expect_manual": {
            "input_file_validations": "/apps/DPO/test1.csv",
            "validations": {
                "submissions": {
                    "filename": "/apps/DPO/test1.csv",
                    "s3_path": "test/DPO/test1.csv"
                },
                "bdr": {
                    "filename": "/apps/DPO/test2.csv",
                    "s3_path": "test/DPO/test2.csv"
                }
            }
        }
    }
]

# Function to upload files to S3
def upload_to_s3(local_path, s3_path):
    try:
        s3.upload_file(local_path, 'your-bucket-name', s3_path)
        print(f"Successfully uploaded {local_path} to s3://{s3_path}")
    except Exception as e:
        print(f"Error uploading {local_path}: {e}")

# Iterate through the data and upload the files
for entry in data:
    # Input file to be manually uploaded
    input_manual_upload = entry["input_manual_upload"]
    upload_to_s3(input_manual_upload["filename"], input_manual_upload["s3_path"])

    # Expect manual file and its validations
    expect_manual = entry["expect_manual"]
    upload_to_s3(expect_manual["input_file_validations"], expect_manual["s3_path"])

    # Validations files
    validations = expect_manual["validations"]
    for key, value in validations.items():
        upload_to_s3(value["filename"], value["s3_path"])


