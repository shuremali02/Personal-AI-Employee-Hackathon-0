#!/usr/bin/env python3
"""
Quick Gmail OAuth Setup for Personal Accounts
"""

import os
import json
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def setup_oauth_for_personal_gmail():
    """Set up OAuth for personal Gmail account."""
    creds = None

    # Token file stores the user's access and refresh tokens
    token_file = "gmail-user-token.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Token refresh failed: {e}")
                # Delete the token file to force re-authentication
                if os.path.exists(token_file):
                    os.remove(token_file)

        if not creds:
            # For OAuth setup, you need to create credentials in Google Cloud Console
            print("To set up Gmail access for personal account:")
            print("1. Go to: https://console.cloud.google.com/")
            print("2. Create a new project or select existing one")
            print("3. Enable Gmail API")
            print("4. Go to 'Credentials' -> 'Create Credentials' -> 'OAuth 2.0 Client IDs'")
            print("5. Choose 'Desktop application' as application type")
            print("6. Download the credentials JSON file")
            print("7. Rename it to 'gmail-oauth-credentials.json' in this directory")
            print()
            print("After setting up OAuth credentials, run this again.")
            return False

    return True

if __name__ == "__main__":
    print("Gmail OAuth Setup Helper")
    print("="*30)
    setup_oauth_for_personal_gmail()