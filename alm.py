import requests
from requests.auth import HTTPBasicAuth

# ALM Server Details
server_url = "https://{server-address}/qcbin"
auth_endpoint = f"{server_url}/authentication-point/authenticate"
test_endpoint = f"{server_url}/rest/domains/{domain}/projects/{project}/tests"

# User credentials
username = "your-username"
password = "your-password"

# Step 1: Authenticate
session = requests.Session()
auth_response = session.post(auth_endpoint, auth=HTTPBasicAuth(username, password))

if auth_response.status_code == 200:
    print("Authenticated successfully!")
else:
    print(f"Authentication failed: {auth_response.status_code}")
    exit()

# Step 2: Fetch Test IDs
headers = {"Accept": "application/json"}
test_response = session.get(test_endpoint, headers=headers)

if test_response.status_code == 200:
    test_data = test_response.json()
    for test in test_data.get('entities', []):
        test_id = next(field['values'][0]['value'] for field in test['Fields'] if field['Name'] == 'id')
        test_name = next(field['values'][0]['value'] for field in test['Fields'] if field['Name'] == 'name')
        print(f"Test ID: {test_id}, Test Name: {test_name}")
else:
    print(f"Failed to fetch tests: {test_response.status_code}")



curl -X GET \
https://{server-address}/qcbin/rest/domains/{domain}/projects/{project}/tests \
-H "Accept: application/json" \
-u username:password



curl -u username:password https://{server-address}/qcbin/authentication-point/authenticate

