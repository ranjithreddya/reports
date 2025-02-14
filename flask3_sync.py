import os
import pandas as pd
import boto3

# AWS S3 configuration
AWS_BUCKET_NAME = 'your-s3-bucket-name'
AWS_REGION = 'your-region'

# Initialize S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)

def convert_xlsx_to_csv(xlsx_file):
    """Converts the given xlsx file to a CSV file."""
    csv_file = xlsx_file.replace('.xlsx', '.csv')
    # Load the Excel file into pandas DataFrame
    df = pd.read_excel(xlsx_file, engine='openpyxl')
    # Save as CSV
    df.to_csv(csv_file, index=False)
    return csv_file

def upload_to_s3(file_path, s3_path):
    """Uploads a file to the specified S3 path."""
    try:
        s3_client.upload_file(file_path, AWS_BUCKET_NAME, s3_path)
        print(f"Uploaded {file_path} to s3://{AWS_BUCKET_NAME}/{s3_path}")
    except Exception as e:
        print(f"Failed to upload {file_path} to S3: {str(e)}")

def process_esma_folder(esma_folder):
    """Process the ESMA folder: Convert .xlsx to .csv and upload to S3."""
    for root, dirs, files in os.walk(esma_folder):
        for file in files:
            if file.endswith('.xlsx'):
                xlsx_file = os.path.join(root, file)
                
                # Convert .xlsx to .csv
                csv_file = convert_xlsx_to_csv(xlsx_file)
                
                # Generate S3 path (preserving folder structure)
                relative_path = os.path.relpath(xlsx_file, esma_folder)
                s3_path = os.path.join('ESMA', relative_path.replace('.xlsx', '.csv'))
                
                # Upload the CSV file to AWS S3
                upload_to_s3(csv_file, s3_path)

def copy_folder_to_s3(folder_path, s3_base_path):
    """Recursively copies the entire folder and its contents to S3."""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Create the corresponding S3 path based on the folder structure
            relative_path = os.path.relpath(file_path, folder_path)
            s3_path = os.path.join(s3_base_path, relative_path)
            
            # Upload file to S3
            upload_to_s3(file_path, s3_path)

def process_jurisdictions(jurisdiction_folder, jurisdiction_name):
    """Processes a jurisdiction folder."""
    if jurisdiction_name == 'ESMA':
        # For ESMA, convert .xlsx to .csv and upload
        print(f"Processing ESMA folder and converting .xlsx to .csv...")
        process_esma_folder(jurisdiction_folder)
    else:
        # For other jurisdictions (ASIC, HKMA), directly copy subfolders to S3
        print(f"Processing {jurisdiction_name} folder and copying subfolders to S3...")
        copy_folder_to_s3(jurisdiction_folder, jurisdiction_name)

def main():
    # List of jurisdiction folders to process
    jurisdictions = ['ASIC', 'ESMA', 'HKMA']
    
    # Base directory where the jurisdiction folders exist
    base_directory = '/Users/ranjithrreddyabbidi/test'
    
    for jurisdiction in jurisdictions:
        jurisdiction_folder = os.path.join(base_directory, jurisdiction)
        
        if os.path.exists(jurisdiction_folder):
            process_jurisdictions(jurisdiction_folder, jurisdiction)
        else:
            print(f"Jurisdiction folder {jurisdiction} does not exist.")

if __name__ == '__main__':
    main()
