#!/usr/bin/env python3
"""
Helper script to set up Gmail API credentials for the AI Employee system.
"""

import os
import sys
from pathlib import Path
import subprocess


def check_env_vars():
    """Check if Gmail environment variables are set."""
    env_vars = {
        'GMAIL_CLIENT_ID': os.getenv('GMAIL_CLIENT_ID'),
        'GMAIL_CLIENT_SECRET': os.getenv('GMAIL_CLIENT_SECRET'),
        'GMAIL_REDIRECT_URI': os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:8080/callback')
    }

    print("🔍 Checking Gmail Environment Variables:")
    all_set = True

    for var_name, var_value in env_vars.items():
        status = "✅ SET" if var_value else "❌ NOT SET"
        value_display = var_value[:20] + "..." if var_value and len(var_value) > 20 else (var_value if var_value else "None")
        print(f"   {var_name}: {status} ({value_display})")

        if not var_value:
            all_set = False

    return all_set, env_vars


def show_setup_instructions():
    """Show instructions for setting up Gmail credentials."""
    print("\n🔐 Gmail API Setup Instructions:")
    print("="*50)
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new Google Cloud Project or select existing one")
    print("3. Enable the Gmail API for your project")
    print("4. Go to 'Credentials' and create OAuth 2.0 Client ID")
    print("5. Download the credentials JSON file")
    print("6. Set the following environment variables:")
    print()
    print("   export GMAIL_CLIENT_ID='your_actual_client_id'")
    print("   export GMAIL_CLIENT_SECRET='your_actual_client_secret'")
    print("   export GMAIL_REDIRECT_URI='http://localhost:8080/callback'")
    print()
    print("   Or add them to your ~/.bashrc or ~/.zshrc file:")
    print("   echo 'export GMAIL_CLIENT_ID=\"your_client_id\"' >> ~/.bashrc")
    print("   echo 'export GMAIL_CLIENT_SECRET=\"your_client_secret\"' >> ~/.bashrc")
    print("   echo 'export GMAIL_REDIRECT_URI=\"http://localhost:8080/callback\"' >> ~/.bashrc")
    print("   source ~/.bashrc")
    print()
    print("💡 Alternative: Place 'gmail-credentials.json' in project root directory")


def test_gmail_watcher():
    """Test if the Gmail watcher can run."""
    print("\n🧪 Testing Gmail Watcher Setup...")

    # Check if we can import required modules
    try:
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request
        print("✅ Gmail API modules are available")
    except ImportError as e:
        print(f"❌ Missing Gmail API modules: {e}")
        print("   Run: pip install google-api-python-client google-auth google-auth-oauthlib")
        return False

    # Check environment variables
    all_set, env_vars = check_env_vars()

    if all_set:
        print("✅ All required environment variables are set!")
        print("\n🚀 To start the Gmail watcher:")
        print("   cd /mnt/e/Personal\\ AI\\ Employee\\ Hackathon\\ 0")
        print("   source venv/bin/activate")
        print("   python src/watchers/gmail_watcher.py")
        return True
    else:
        print("❌ Some environment variables are missing.")
        show_setup_instructions()
        return False


def main():
    print("🔐 Gmail API Credentials Setup Helper")
    print("="*50)

    success = test_gmail_watcher()

    if success:
        print("\n🎉 Gmail watcher is ready to use!")
        print("It will monitor your Gmail for new emails and create entries in Needs_Action folder.")
    else:
        print("\n❗ Please complete the setup before running the Gmail watcher.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())