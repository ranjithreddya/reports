import requests
import json
import urllib.parse
import datetime

# Custom function to handle non-serializable types
def json_serial(obj):
    """Custom serializer for non-serializable objects."""
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()  # Convert datetime to ISO string
    elif isinstance(obj, set):
        return list(obj)  # Convert sets to lists
    raise TypeError(f"Object of type '{type(obj)}' is not serializable")

# Function to recursively convert sets to lists in any nested structure (dicts, lists)
def convert_sets_to_lists(data):
    """Recursively convert sets to lists in a dictionary or list."""
    if isinstance(data, set):
        return list(data)  # Convert a set to a list
    elif isinstance(data, dict):
        return {key: convert_sets_to_lists(value) for key, value in data.items()}  # Recurse through dictionary
    elif isinstance(data, list):
        return [convert_sets_to_lists(item) for item in data]  # Recurse through list
    return data  # Base case: return data if it's not a set, dict, or list

# Base URL
base_url = "https://almdev.dtcc.com/qcbin/rest/domains/domain/projects/tests"

# Raw query string exactly as required
query = "{parent-id[^subject\\GTR\\2024 production release^]}"

# Headers (if needed, adjust based on your authentication method)
headers = {
    "Authorization": "Basic YOUR_AUTH_TOKEN",  # Replace with your actual auth token
    "Content-Type": "application/json"
}

# File to write the results
output_file = 'alm_test_cases.json'

# Initialize the file by creating an empty JSON structure
with open(output_file, 'w') as file:
    json.dump({"entities": []}, file)  # Initialize the file with an empty 'entities' list

# Pagination setup
start = 1  # Start with the first page
page_size = 2000  # The number of items per page (based on your request to use page-size=2000)

# Loop to fetch all pages
while True:
    # Build the URL with pagination parameters
    final_url = f"{base_url}?query={urllib.parse.quote(query)}&page-size={page_size}&start-index={start}"

    # Send the GET request with the constructed URL
    response = requests.get(final_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the response as JSON
        data = response.json()

        # Debugging: Print the structure of the response
        print(f"Response data (partial): {json.dumps(data, indent=4)[:200]}...")  # Print the first 200 characters for inspection

        # Check if the response contains the expected list of entities
        if 'entities' in data:  # Adjust the key here based on your actual response structure
            records = data['entities']  # Assuming the records are inside 'entities' key
            
            # Convert sets to lists in the response
            records = convert_sets_to_lists(records)  # Ensure no sets in 'records'

            # Append the results to the output file in the required format
            with open(output_file, 'r+') as file:
                file_data = json.load(file)
                
                # Convert sets to lists in the existing data
                file_data = convert_sets_to_lists(file_data)  # Ensure no sets in 'file_data'
                
                # Add the fetched records to the 'entities' list
                file_data['entities'].extend(records)  # Add the results from this page
                
                file.seek(0)  # Move the cursor to the beginning of the file
                json.dump(file_data, file, indent=4, default=json_serial)  # Write the updated content

            # Debugging: Print how many records were fetched
            print(f"Fetched {len(records)} records, starting at {start}.")

            # Check if there are more pages to fetch
            if len(records) < page_size:  # If fewer records than the page-size, we are at the last page
                print(f"Fetched all {start - 1 + len(records)} records.")
                break
            else:
                start += page_size  # Move to the next page using start-index
        else:
            print("Error: Expected 'entities' key not found in response.")
            break
    else:
        print(f"Error: {response.status_code}, {response.text}")
        break

# Print the total number of results fetched
print(f"Results written to {output_file}")



######################################################################################

import json
import requests
from django.conf import settings
import urllib
import time

class ALMAPIClient:
    def __init__(self):
        self.session = requests.Session()
        self.client_id = settings.ALM_CLIENT_ID  
        self.client_secret = settings.ALM_CLIENT_SECRET  
        self.alm_api_url = settings.ALM_API_URL 
        self.token_url = 'https://almdev.dtcc.com/qcbin/rest/oauth2/login'
        self.logout_url = 'https://almdev.dtcc.com/qcbin/authentication-point/logout'

        # SSL certificate paths
        self.ssl_cert_path = settings.SSL_CERT_PATH  # Full path to .pem file (including certificate and private key)
        self.ssl_cert_key_path = settings.SSL_CERT_KEY_PATH  # Optional: full path to the key if it's separate from the cert

        # Tracking state
        self.output_file = 'alm_test_cases.json'

    def login(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        try:
            # Provide both certificate and private key if they're separate files
            cert = (self.ssl_cert_path, self.ssl_cert_key_path) if self.ssl_cert_key_path else self.ssl_cert_path

            token_response = self.session.post(
                self.token_url, 
                data=payload, 
                cert=cert,  # Use the certificate for authentication
                verify=self.ssl_cert_path  # Verify the server certificate
            )

            if token_response.status_code == 200:
                print("Login successful!")
                return True
            else:
                print(f"Failed to obtain access token: {token_response.status_code} - {token_response.text}")
                return False
        except requests.exceptions.SSLError as e:
            print(f"SSL Error: {e}")
            return False

    def fetch_test_cases(self):
        start = 1
        page_size = 2000
        last_successful_index = self.load_progress()

        while True:
            headers = {
                "Content-Type": "application/json"
            }

            final_url = f"{self.alm_api_url}?query={urllib.parse.quote('query')}&page-size={page_size}&start-index={start}"

            try:
                # Provide both certificate and private key if they're separate files
                cert = (self.ssl_cert_path, self.ssl_cert_key_path) if self.ssl_cert_key_path else self.ssl_cert_path

                response = requests.get(
                    final_url,
                    headers=headers,
                    cert=cert,
                    verify=self.ssl_cert_path  # Verify the server certificate
                )

                if response.status_code == 200:
                    data = response.json()

                    if 'entities' in data:
                        records = data['entities']
                        records = self.convert_sets_to_lists(records)

                        with open(self.output_file, 'r+') as file:
                            file_data = json.load(file)
                            file_data = self.convert_sets_to_lists(file_data)
                            file_data['entities'].extend(records)
                            file.seek(0)
                            json.dump(file_data, file, indent=4, default=self.json_serial)

                        if len(records) < page_size:
                            print("All records fetched.")
                            break
                        else:
                            start += page_size
                            self.save_progress(start)  # Save the last index where we stopped
                    else:
                        print("No entities found in the response.")
                        break
                else:
                    print(f"Request failed with status code {response.status_code}. Retrying...")
                    if response.status_code == 401:  # Unauthorized, try re-authentication
                        print("Authentication failed, re-authenticating...")
                        if self.login():
                            continue  # Retry after re-authentication
                        else:
                            break
                    else:
                        break

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
                break

    def logout(self):
        try:
            # Provide both certificate and private key if they're separate files
            cert = (self.ssl_cert_path, self.ssl_cert_key_path) if self.ssl_cert_key_path else self.ssl_cert_path

            logout_response = self.session.delete(
                self.logout_url, 
                cert=cert,  # Use the certificate for authentication
                verify=self.ssl_cert_path  # Verify the server certificate
            )

            if logout_response.status_code == 200:
                print("Logged out successfully.")
            else:
                print(f"Failed to log out: {logout_response.status_code} - {logout_response.text}")
        except requests.exceptions.SSLError as e:
            print(f"SSL Error during logout: {e}")

        self.session.close()

    def save_progress(self, start_index):
        """Save the last successful index to continue from where we left off."""
        with open('progress.json', 'w') as progress_file:
            json.dump({'start_index': start_index}, progress_file)

    def load_progress(self):
        """Load the last saved index where we stopped fetching data."""
        try:
            with open('progress.json', 'r') as progress_file:
                progress_data = json.load(progress_file)
                return progress_data.get('start_index', 1)
        except (FileNotFoundError, json.JSONDecodeError):
            return 1  # Start from index 1 if no progress file exists

    def convert_sets_to_lists(self, records):
        # Your conversion logic here if required
        return records

    def json_serial(self, obj):
        # Define how to serialize any custom objects if needed
        return str(obj)

def main():
    alm_client = ALMAPIClient()

    if alm_client.login():
        alm_client.fetch_test_cases()
        alm_client.logout()

if __name__ == "__main__":
    main()

