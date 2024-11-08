import requests
from django.conf import settings

class ALMAPIClient:
    def __init__(self):
        self.session = requests.Session()
        self.client_id = settings.ALM_CLIENT_ID  # Assuming client_id is set in settings.py
        self.client_secret = settings.ALM_CLIENT_SECRET  # Assuming client_secret is set in settings.py
        self.alm_api_url = settings.ALM_API_URL  # Assuming alm_api_url is set in settings.py
        self.token_url = 'https://almdev.dtcc.com/qcbin/rest/oauth2/login'  # OAuth2 token URL
        self.logout_url = 'https://almdev.dtcc.com/qcbin/authentication-point/logout'  # Logout URL
        self.revoke_url = 'https://almdev.dtcc.com/qcbin/rest/oauth2/revoke'  # Token revoke URL (optional)

    def login(self):
        """Login to the ALM API and retrieve the access token."""
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        # Send POST request to get the access token
        token_response = self.session.post(self.token_url, data=payload)

        if token_response.status_code == 200:
            # Extract the access token from the response
            self.access_token = token_response.json().get('access_token')
            print("Login successful!")
            return True
        else:
            print(f"Failed to obtain access token: {token_response.status_code} - {token_response.text}")
            return False

    def fetch_test_cases(self):
        """Fetch test cases from the ALM API."""
        if not hasattr(self, 'access_token'):
            print("Access token is not set. Please login first.")
            return

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }

        # Send GET request to fetch test cases
        test_response = self.session.get(self.alm_api_url, headers=headers)

        if test_response.status_code == 200:
            # Print or process the test cases data
            print(test_response.json().get('entities'))
        else:
            print(f"Failed to fetch test cases: {test_response.status_code} - {test_response.text}")

    def logout(self):
        """Log out from the ALM API and revoke the token (if necessary)."""
        # Send DELETE request to log out
        logout_response = self.session.delete(self.logout_url)

        if logout_response.status_code == 200:
            print("Logged out successfully.")
            # Optionally revoke the access token (if the API supports it)
            self.revoke_token()  # Optional, if the API supports token revocation
            # Clear session cookies to prevent future automatic reuse
            self.session.cookies.clear()
            self.session.close()
        else:
            print(f"Failed to log out: {logout_response.status_code} - {logout_response.text}")
    
    def revoke_token(self):
        """Revoke the OAuth access token explicitly (optional, if needed)."""
        revoke_payload = {'token': self.access_token}
        revoke_response = self.session.post(self.revoke_url, data=revoke_payload)

        if revoke_response.status_code == 200:
            print("Token revoked successfully.")
        else:
            print(f"Failed to revoke token: {revoke_response.status_code} - {revoke_response.text}")


def main():
    # Initialize the ALM API Client
    alm_client = ALMAPIClient()

    # Step 1: Log in to ALM API
    if alm_client.login():
        # Step 2: Fetch test cases from ALM
        alm_client.fetch_test_cases()

        # Step 3: Log out after fetching test cases
        alm_client.logout()


if __name__ == "__main__":
    main()


###################################################################################################################################
