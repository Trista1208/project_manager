# src/core/create_token.py
# Run this once to create token.json from credentials.json

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def create_token():
    creds = None

    # Check if token.json already exists
    if os.path.exists("token.json"):
        print("token.json already exists!")
        return

    # Check if credentials.json exists
    if not os.path.exists("credentials.json"):
        print("ERROR: credentials.json not found!")
        print("Place credentials.json in the same directory as this script.")
        return

    # Create token from credentials
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Save token.json
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    print("✅ token.json created successfully!")


if __name__ == "__main__":
    create_token()



