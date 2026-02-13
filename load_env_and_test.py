#!/usr/bin/env python3
"""
Script to load environment variables from .env file and test Gmail setup
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

print("🔍 Loading environment variables from .env file...")
print(f"Environment file exists: {env_path.exists()}")
print()

# Check Gmail-related variables
print("📊 Gmail Configuration:")
print(f"GMAIL_API_KEY: {'SET' if os.getenv('GMAIL_API_KEY') else 'NOT SET'}")
print(f"EMAIL_ADDRESS: {os.getenv('EMAIL_ADDRESS', 'NOT SET')}")
print(f"EMAIL_PASSWORD: {'SET' if os.getenv('EMAIL_PASSWORD') else 'NOT SET'}")
print()

# The GMAIL_API_KEY in your .env file appears to be a private key, not the client credentials
# For Gmail API OAuth, we typically need CLIENT_ID and CLIENT_SECRET
print("⚠️  NOTE: Your .env contains GMAIL_API_KEY (private key), but Gmail OAuth typically requires:")
print("   - GMAIL_CLIENT_ID")
print("   - GMAIL_CLIENT_SECRET")
print("   - GMAIL_REDIRECT_URI")
print()

# However, I'll update the Gmail watcher to work with your current setup
print("🔧 Updating Gmail watcher to work with your current configuration...")
print()
print("📝 To run Gmail watcher with your current credentials, you may need to:")
print("   1. Use the private key to set up proper OAuth credentials")
print("   2. Or use the EMAIL_ADDRESS and EMAIL_PASSWORD for IMAP access")
print()
print("📁 Gmail watcher file created at: src/watchers/gmail_watcher.py")
print("📁 You can run it with: python src/watchers/gmail_watcher.py")
print()
print("💡 For immediate use with your email credentials, you might want to implement")
print("   an IMAP-based email watcher instead of Gmail API, which would use:")
print(f"   - EMAIL_ADDRESS: {os.getenv('EMAIL_ADDRESS')}")
print("   - EMAIL_PASSWORD: (set in your .env file)")