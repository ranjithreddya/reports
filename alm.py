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



################################
import requests
from django.conf import settings

class ALMAPIClient:
    def __init__(self):
        self.client_id = settings.ALM_CLIENT_ID
        self.client_secret = settings.ALM_CLIENT_SECRET
        self.token_url = settings.ALM_TOKEN_URL
        self.alm_api_url = settings.ALM_API_URL
        self.access_token = None

    def authenticate(self):
        """Authenticate using client credentials and obtain an access token."""
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        token_response = requests.post(self.token_url, data=payload)

        if token_response.status_code == 200:
            self.access_token = token_response.json().get('access_token')
            print(f"Access token: {self.access_token}")
        else:
            raise Exception(f"Failed to obtain access token: {token_response.status_code} - {token_response.text}")

    def get_tests(self):
        """Fetch test cases from the ALM API."""
        if not self.access_token:
            self.authenticate()

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }

        test_response = requests.get(self.alm_api_url, headers=headers)

        if test_response.status_code == 200:
            return test_response.json().get('entities', [])
        else:
            raise Exception(f"Failed to fetch test cases: {test_response.status_code} - {test_response.text}")

    def get_test_ids_and_names(self):
        """Extract test IDs and names from the API response."""
        tests = self.get_tests()
        return [(next(field['values'][0]['value'] for field in test['Fields'] if field['Name'] == 'id'),
                 next(field['values'][0]['value'] for field in test['Fields'] if field['Name'] == 'name'))
                for test in tests]

#settings.py
import os

ALM_CLIENT_ID = os.getenv('ALM_CLIENT_ID')
ALM_CLIENT_SECRET = os.getenv('ALM_CLIENT_SECRET')
ALM_TOKEN_URL = os.getenv('ALM_TOKEN_URL')  # e.g., "https://{auth-server-address}/oauth/token"
ALM_API_URL = os.getenv('ALM_API_URL')  # e.g., "https://{alm-server-address}/qcbin/rest/domains/{domain}/projects/{project}/tests"


#any views.py
from django.http import JsonResponse
from .services.alm_api import ALMAPIClient

def fetch_alm_tests(request):
    try:
        alm_client = ALMAPIClient()
        test_ids_and_names = alm_client.get_test_ids_and_names()
        return JsonResponse({'tests': test_ids_and_names})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


#########################################


alm wrapper:

from functools import wraps
from django.http import JsonResponse
from .services.alm_api import ALMAPIClient

def alm_authentication_required(view_func):
    """Decorator to ensure ALM authentication with client ID and secret."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        client_id = request.META.get('HTTP_CLIENT_ID')
        client_secret = request.META.get('HTTP_CLIENT_SECRET')

        if not client_id or not client_secret:
            return JsonResponse({'error': 'Client ID and Client Secret are required.'}, status=400)

        try:
            # Initialize ALM API client with client ID and secret
            alm_client = ALMAPIClient(client_id, client_secret)
            alm_client.authenticate()  # Ensure valid authentication
            
            # Pass the client object to the view for API calls
            kwargs['alm_client'] = alm_client
        except Exception as e:
            return JsonResponse({'error': f'ALM authentication failed: {str(e)}'}, status=500)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def alm_authentication_wrapper(view_func):
    """Wrapper to apply the ALM authentication decorator."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # You can add additional logging or preprocessing here if needed
        
        return alm_authentication_required(view_func)(request, *args, **kwargs)

    return wrapper


class MyView(View):
    @alm_authentication_wrapper
    def get(self, request, *args, **kwargs):
        alm_client = kwargs.get('alm_client')
        # Use alm_client to perform your API operations
        return JsonResponse({'message': 'Success!'}, status=200)



# your_app/views.py

from django.views import View
from django.http import JsonResponse
from .decorators.alm_auth import alm_authentication_wrapper

class MyView(View):
    @alm_authentication_wrapper
    def get(self, request, *args, **kwargs):
        alm_client = kwargs.get('alm_client')
        
        # Define the domain and project
        domain = 'your_domain'  # Replace with your actual domain
        project = 'your_project'  # Replace with your actual project
        
        # Construct the endpoint URL
        server_url = "https://{server-address}/qcbin"
        test_endpoint = f"{server_url}/rest/domains/{domain}/projects/{project}/tests"
        
        try:
            # Call the test endpoint using the alm_client
            response = alm_client.get(test_endpoint)  # Adjust this method based on your client implementation
            
            # Assuming the response is JSON; you might need to handle it accordingly
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            return JsonResponse({'error': f'Error calling ALM test endpoint: {str(e)}'}, status=500)




# your_app/services/alm_api.py
# your_app/services/alm_api.py

import requests

class ALMAPIClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.base_url = "https://{server-address}/qcbin"  # Adjust this accordingly

    def authenticate(self):
        """Authenticate to the ALM API."""
        auth_url = f"{self.base_url}/authentication-point/authenticate"
        credentials = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            # Perform the POST request to authenticate
            response = self.session.post(auth_url, json=credentials)

            # Check if the authentication was successful
            if response.status_code == 200:
                print("Authentication successful.")
            else:
                raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

        except Exception as e:
            raise Exception(f"Error during authentication: {str(e)}")

    def get(self, url):
        """Make a GET request to the specified URL."""
        return self.session.get(url, auth=(self.client_id, self.client_secret))




################
# your_app/views.py

from django.views import View
from django.http import JsonResponse
import requests

class ALMAPIClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.base_url = "https://{server-address}/qcbin"  # Adjust this accordingly

    def authenticate(self):
        """Authenticate to the ALM API using the login API."""
        login_url = f"{self.base_url}/authentication-point/authenticate"
        
        # Payload for authentication
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = self.session.post(login_url, json=payload)

        # Check if the authentication was successful
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

    def get_tests(self, domain, project):
        """Retrieve tests from the ALM API."""
        tests_endpoint = f"{self.base_url}/rest/domains/{domain}/projects/{project}/tests"
        return self.session.get(tests_endpoint)

class TestsView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve client ID and secret from request headers
        client_id = request.META.get('HTTP_CLIENT_ID')
        client_secret = request.META.get('HTTP_CLIENT_SECRET')

        if not client_id or not client_secret:
            return JsonResponse({'error': 'Client ID and Client Secret are required.'}, status=400)

        # Initialize the ALM API client
        alm_client = ALMAPIClient(client_id, client_secret)

        # Authenticate
        try:
            alm_client.authenticate()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Define the domain and project
        domain = 'your_domain'  # Replace with your actual domain
        project = 'your_project'  # Replace with your actual project
        
        # Call the tests endpoint
        try:
            response = alm_client.get_tests(domain, project)

            # Return the response from ALM
            return JsonResponse(response.json(), status=response.status_code)
        except Exception as e:
            return JsonResponse({'error': f'Error retrieving tests: {str(e)}'}, status=500)


#####
import requests

class ALMAPIClient:
    def __init__(self, client_id, client_secret, server_address):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.base_url = f"https://{server_address}/qcbin"  # Construct the base URL

    def authenticate(self):
        """Authenticate to the ALM API using the login API."""
        login_url = f"{self.base_url}/authentication-point/authenticate"
        
        # Payload for authentication
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        response = self.session.post(login_url, json=payload)

        # Check if the authentication was successful
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

    def get_tests(self, domain, project):
        """Retrieve tests from the ALM API."""
        tests_endpoint = f"{self.base_url}/rest/domains/{domain}/projects/{project}/tests"
        return self.session.get(tests_endpoint)

def main():
    # Input your credentials and server details
    client_id = input("Enter your Client ID: ")
    client_secret = input("Enter your Client Secret: ")
    server_address = input("Enter the server address (without https://): ")
    domain = input("Enter the domain: ")
    project = input("Enter the project: ")

    # Initialize the ALM API client
    alm_client = ALMAPIClient(client_id, client_secret, server_address)

    # Authenticate
    try:
        alm_client.authenticate()
        print("Authentication successful.")
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return

    # Call the tests endpoint
    try:
        response = alm_client.get_tests(domain, project)

        # Check if the request was successful
        if response.status_code == 200:
            print("Tests retrieved successfully:")
            print(response.json())  # Print the retrieved tests
        else:
            print(f"Error retrieving tests: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error retrieving tests: {str(e)}")

if __name__ == "__main__":
    main()

