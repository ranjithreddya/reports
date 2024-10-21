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


import requests

# ALM server details
token_url = "https://{auth-server-address}/oauth/token"  # OAuth 2.0 token endpoint
alm_base_url = "https://{server-address}/qcbin/rest/domains/{domain}/projects/{project}/tests"

# OAuth 2.0 client credentials
client_id = "your-client-id"
client_secret = "your-client-secret"
scope = "alm-api-scope"  # Replace with appropriate scope if needed (depends on ALM setup)
grant_type = "client_credentials"

# Step 1: Get OAuth 2.0 access token
payload = {
    'grant_type': grant_type,
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope
}

token_response = requests.post(token_url, data=payload)

if token_response.status_code == 200:
    access_token = token_response.json().get('access_token')
    print(f"Access token obtained: {access_token}")
else:
    print(f"Failed to obtain access token: {token_response.status_code}")
    print(token_response.text)
    exit()

# Step 2: Make authenticated request to ALM API using access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'Accept': 'application/json'
}

test_response = requests.get(alm_base_url, headers=headers)

if test_response.status_code == 200:
    test_data = test_response.json()
    for test in test_data.get('entities', []):
        test_id = next(field['values'][0]['value'] for field in test['Fields'] if field['Name'] == 'id')
        test_name = next(field['values'][0]['value'] for field in test['Fields'] if field['Name'] == 'name')
        print(f"Test ID: {test_id}, Test Name: {test_name}")
else:
    print(f"Failed to fetch tests: {test_response.status_code}")
    print(test_response.text)

