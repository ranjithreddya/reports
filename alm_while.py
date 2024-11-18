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
