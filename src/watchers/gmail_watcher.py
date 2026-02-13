#!/usr/bin/env python3
"""
Gmail Watcher for AI Employee Vault

Monitors Gmail for new important/unread messages and creates markdown files in
the Needs_Action directory with appropriate metadata.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GmailWatcher:
    """Class to handle Gmail monitoring and processing."""

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, vault_needs_action_dir, credentials_file=None):
        self.vault_needs_action_dir = Path(vault_needs_action_dir)
        self.credentials_file = credentials_file or "gmail-credentials.json"
        self.service = None
        self.last_check_time = None

    def authenticate(self):
        """Authenticate with Gmail API using stored credentials."""
        creds = None

        # Check for token file first
        token_file = "gmail-token.json"
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    # Delete the token file to force re-authentication
                    if os.path.exists(token_file):
                        os.remove(token_file)
                    creds = None

            if not creds:
                # Try to get credentials from environment variables
                credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH')

                # Prioritize service account credentials (most reliable for automated access)
                if credentials_path and os.path.exists(credentials_path):
                    # Use the service account credentials from the specified path
                    print(f"Using service account credentials from: {credentials_path}")
                    import json
                    from google.oauth2 import service_account

                    with open(credentials_path, 'r') as f:
                        creds_data = json.load(f)

                    # Use service account credentials for Gmail API
                    creds = service_account.Credentials.from_service_account_info(
                        creds_data, scopes=self.SCOPES
                    )
                else:
                    # Fall back to OAuth if no service account credentials
                    client_id = os.getenv('GMAIL_CLIENT_ID')
                    client_secret = os.getenv('GMAIL_CLIENT_SECRET')
                    redirect_uri = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8080/callback')

                    if client_id and client_secret:
                        # Create credentials from environment
                        credentials_info = {
                            "installed": {
                                "client_id": client_id,
                                "client_secret": client_secret,
                                "redirect_uris": [redirect_uri],
                                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                "token_uri": "https://oauth2.googleapis.com/token"
                            }
                        }

                        flow = InstalledAppFlow.from_client_config(credentials_info, self.SCOPES)
                        flow.redirect_uri = redirect_uri
                        creds = flow.run_local_server(port=0)
                    else:
                        # Try to load from default file
                        if os.path.exists(self.credentials_file):
                            flow = InstalledAppFlow.from_client_secrets_file(
                                self.credentials_file, self.SCOPES
                            )
                            creds = flow.run_local_server(port=0)
                        else:
                            print("⚠️  Gmail credentials not found in environment variables.")
                            print("📝 Please set these environment variables:")
                            print("   export GMAIL_CREDENTIALS_PATH='/path/to/your/service-account-credentials.json'")
                            print("   OR for OAuth:")
                            print("   export GMAIL_CLIENT_ID='your_client_id'")
                            print("   export GMAIL_CLIENT_SECRET='your_client_secret'")
                            print("   export GMAIL_REDIRECT_URI='http://localhost:8080/callback'")
                            print("")
                            print("🔄 Or place 'gmail-credentials.json' in the project root directory")
                            raise Exception("No valid Gmail credentials found")

                # Save the credentials for next run (only for user credentials, not service accounts)
                if not hasattr(creds, 'signer'):  # Service accounts don't need token file
                    with open(token_file, 'w') as token:
                        token.write(creds.to_json())

        self.service = build('gmail', 'v1', credentials=creds)
        print("Gmail authentication successful!")

    def get_recent_emails(self, max_results=10):
        """Get recent unread emails from Gmail."""
        try:
            # Format the query for unread emails
            query = "is:unread"

            if self.last_check_time:
                # Only get emails received after the last check
                query += f" after:{self.last_check_time.strftime('%Y/%m/%d')}"

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])

            email_list = []
            for msg in messages:
                email_data = self.get_email_details(msg['id'])
                if email_data:
                    email_list.append(email_data)

            # Update last check time
            self.last_check_time = datetime.now()

            return email_list

        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def get_email_details(self, msg_id):
        """Get detailed information about a specific email."""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            # Extract email headers
            headers = message['payload']['headers']
            email_info = {
                'id': msg_id,
                'subject': '',
                'from': '',
                'to': '',
                'date': '',
                'body': '',
                'labels': message.get('labelIds', [])
            }

            for header in headers:
                name = header['name'].lower()
                value = header['value']
                if name == 'subject':
                    email_info['subject'] = value
                elif name == 'from':
                    email_info['from'] = value
                elif name == 'to':
                    email_info['to'] = value
                elif name == 'date':
                    email_info['date'] = value

            # Extract email body
            if 'parts' in message['payload']:
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        import base64
                        body_data = part['body']['data']
                        email_info['body'] = base64.urlsafe_b64decode(body_data).decode('utf-8')
                        break
                    elif part['mimeType'] == 'text/html':
                        import base64
                        body_data = part['body']['data']
                        email_info['body_html'] = base64.urlsafe_b64decode(body_data).decode('utf-8')
            else:
                # Single part email
                if 'body' in message['payload'] and 'data' in message['payload']['body']:
                    import base64
                    body_data = message['payload']['body']['data']
                    email_info['body'] = base64.urlsafe_b64decode(body_data).decode('utf-8')

            return email_info

        except Exception as e:
            print(f"Error getting email details: {e}")
            return None

    def create_markdown_entry(self, email_info):
        """Create a markdown entry in the Needs_Action directory."""
        try:
            # Generate unique ID based on timestamp and email ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = f"{timestamp}_{email_info['id'][:8]}"

            # Create markdown filename
            safe_subject = "".join(c for c in email_info['subject'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_subject:
                safe_subject = "untitled_email"
            md_filename = f"EMAIL_{unique_id}_{safe_subject[:50]}.md"
            md_filepath = self.vault_needs_action_dir / md_filename

            # Create markdown content
            content = f"""---
title: "Email Processing Request: {email_info['subject']}"
created: {datetime.now().isoformat()}
email_id: "{email_info['id']}"
email_from: "{email_info['from']}"
email_to: "{email_info['to']}"
email_date: "{email_info['date']}"
status: pending
priority: medium
action_required: standard_processing
---

# Email Processing Request

## Email Information
- **Subject**: {email_info['subject']}
- **From**: `{email_info['from']}`
- **To**: `{email_info['to']}`
- **Date**: {email_info['date']}
- **Email ID**: `{email_info['id']}`

## Email Content
{email_info['body'][:2000]}  <!-- Truncated for brevity -->

## Action Required
Review this email and determine appropriate action based on Company Handbook guidelines.

## Instructions
1. Review the email content above
2. Determine appropriate action based on Company Handbook rules
3. Execute the required action
4. Move this file to Done when completed
5. Update Dashboard with status

## Status
- [ ] Email reviewed
- [ ] Action determined
- [ ] Action executed
- [ ] Status updated
"""

            # Write markdown file
            with open(md_filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"Created email entry: {md_filepath}")

            # Mark email as read after processing
            self.mark_email_as_read(email_info['id'])

        except Exception as e:
            print(f"Error creating markdown entry for email: {str(e)}")

    def mark_email_as_read(self, msg_id):
        """Mark an email as read by removing the UNREAD label."""
        try:
            # Remove the UNREAD label
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            print(f"Could not mark email as read: {e}")

    def process_new_emails(self):
        """Process any new unread emails."""
        try:
            emails = self.get_recent_emails()
            processed_count = 0

            for email in emails:
                self.create_markdown_entry(email)
                processed_count += 1

            return processed_count

        except Exception as e:
            print(f"Error processing emails: {str(e)}")
            return 0

    def run_monitoring(self, check_interval=300):  # Default: check every 5 minutes
        """Run continuous monitoring for new emails."""
        print(f"Starting Gmail monitoring...")
        print(f"Checking for new emails every {check_interval} seconds")

        try:
            while True:
                print(f"Checking for new emails at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                count = self.process_new_emails()
                if count > 0:
                    print(f"Processed {count} new emails")
                else:
                    print("No new emails found")

                print(f"Sleeping for {check_interval} seconds...")
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\nStopping Gmail watcher...")
        except Exception as e:
            print(f"Error in monitoring loop: {str(e)}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher for AI Employee Vault')
    parser.add_argument('--vault-dir', default='./AI_Employee_Vault',
                       help='Vault directory containing Needs_Action folder (default: ./AI_Employee_Vault)')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300 for 5 minutes)')

    args = parser.parse_args()

    # Validate vault directory
    vault_dir = Path(args.vault_dir)
    needs_action_dir = vault_dir / 'Needs_Action'

    if not needs_action_dir.exists():
        print(f"Vault Needs_Action directory does not exist: {needs_action_dir}")
        return 1

    # Create the Gmail watcher
    gmail_watcher = GmailWatcher(needs_action_dir)

    try:
        # Authenticate with Gmail
        gmail_watcher.authenticate()

        print("Gmail watcher initialized successfully!")
        print(f"Monitoring Gmail for new emails...")
        print(f"Email entries will be created in: {needs_action_dir}")
        print("Press Ctrl+C to stop.")

        # Run the monitoring
        gmail_watcher.run_monitoring(args.interval)

    except Exception as e:
        print(f"Error initializing Gmail watcher: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    main()