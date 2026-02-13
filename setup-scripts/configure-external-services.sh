#!/bin/bash

# External Service Access Configuration Script for Personal AI Employee Hackathon 0

echo "Configuring external service access..."

# Create external service configuration directory if it doesn't exist
if [ ! -d "config" ]; then
    mkdir -p config
fi

# Create external service access configuration file
cat > config/external-services.json << 'EOF'
{
  "services": {
    "gmail": {
      "enabled": false,
      "api_enabled": false,
      "credentials_required": true,
      "oauth_required": true,
      "scopes": [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send"
      ]
    },
    "whatsapp": {
      "enabled": false,
      "web_enabled": true,
      "credentials_required": true,
      "session_required": true
    },
    "banking": {
      "enabled": false,
      "api_enabled": false,
      "credentials_required": true,
      "api_key_required": true
    }
  },
  "watchers": {
    "gmail_watcher": {
      "enabled": false,
      "poll_interval": 60,
      "actions": ["check_new_emails", "forward_important", "schedule_responses"]
    },
    "whatsapp_watcher": {
      "enabled": false,
      "poll_interval": 30,
      "actions": ["check_messages", "auto_respond", "escalate_issues"]
    },
    "finance_watcher": {
      "enabled": false,
      "poll_interval": 300,
      "actions": ["monitor_transactions", "alert_unusual_activity", "generate_reports"]
    }
  },
  "security": {
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 60
    },
    "authentication_cache": {
      "enabled": true,
      "ttl_seconds": 3600
    },
    "connection_timeout": 30
  }
}
EOF

echo "✓ Created external service configuration file"

# Create Gmail API configuration documentation
cat > docs/gmail-api-setup.md << 'EOF'
# Gmail API Setup Guide

## Prerequisites
- Google account with Gmail enabled
- Google Cloud Platform project
- Enabled Gmail API in Google Cloud Console

## Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable billing for the project (if required)

### 2. Enable Gmail API
1. In Google Cloud Console, go to APIs & Services > Library
2. Search for "Gmail API"
3. Click "Enable" for the Gmail API

### 3. Create OAuth 2.0 Credentials
1. Go to APIs & Services > Credentials
2. Click "Create Credentials" > "OAuth 2.0 Client IDs"
3. Configure the OAuth consent screen
4. Download the credentials JSON file
5. Rename to `gmail-credentials.json`

### 4. Configure Application
1. Place `gmail-credentials.json` in the project root
2. Update `.env` file with:
   ```
   GMAIL_CLIENT_ID=your_client_id
   GMAIL_CLIENT_SECRET=your_client_secret
   GMAIL_REDIRECT_URI=http://localhost:8080/callback
   ```

### 5. Authorization Flow
The application will guide you through the OAuth flow to obtain access tokens.

## Required Scopes
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails

## Rate Limits
- 250 units per day
- 10 units per 100 seconds per user
EOF

echo "✓ Created Gmail API setup documentation"

# Create WhatsApp Web configuration documentation
cat > docs/whatsapp-web-setup.md << 'EOF'
# WhatsApp Web Session Setup Guide

## Prerequisites
- WhatsApp account on mobile device
- Stable internet connection
- Chrome or Firefox browser

## Setup Steps

### 1. QR Code Authentication
1. The application will launch a browser instance
2. Navigate to web.whatsapp.com
3. Scan the QR code with your phone's camera
4. Session will be saved for future use

### 2. Session Persistence
- Sessions are stored in the `sessions/` directory
- Session cookies are saved for continued access
- Sessions expire periodically and need re-authentication

### 3. Configuration
Update `.env` file with:
```
WHATSAPP_HEADLESS_MODE=true
WHATSAPP_AUTO_RESTART=true
WHATSAPP_SESSION_TIMEOUT=3600
```

## Capabilities
- Read incoming messages
- Send automated responses
- Manage contacts
- Handle media files

## Limitations
- Requires phone to remain online
- WhatsApp may detect automation and restrict access
- Rate limits apply to message sending
EOF

echo "✓ Created WhatsApp Web setup documentation"

# Create banking API configuration documentation
cat > docs/banking-api-setup.md << 'EOF'
# Banking API Setup Guide

## Supported Banks
This framework supports integration with various banking APIs that provide transaction monitoring capabilities.

## Setup Steps

### 1. Obtain API Credentials
1. Contact your bank to request API access
2. Register your application if required
3. Obtain API key and secret
4. Understand rate limits and usage policies

### 2. Configuration
Update `.env` file with:
```
BANKING_API_BASE_URL=https://api.yourbank.com
BANKING_API_KEY=your_api_key
BANKING_API_SECRET=your_api_secret
BANKING_ACCOUNT_ID=your_account_id
BANKING_WEBHOOK_URL=https://yourdomain.com/webhook/banking
```

### 3. Security Considerations
- Use HTTPS for all API calls
- Implement proper authentication
- Store credentials securely
- Monitor API usage for anomalies

## Common Endpoints
- GET /accounts/{id}/transactions - Retrieve transactions
- GET /accounts/{id}/balance - Get account balance
- POST /accounts/{id}/notifications - Set up notifications

## Rate Limits
- Varies by institution (typically 1000-10000 requests/day)
EOF

echo "✓ Created banking API setup documentation"

# Create external service access verification script
cat > setup-scripts/verify-external-services.py << 'EOF'
#!/usr/bin/env python3
"""
External Service Access Verification Script
Checks connectivity and configuration for external services
"""

import json
import os
import sys
from typing import Dict, List, Tuple


def verify_gmail_config() -> Tuple[bool, List[str]]:
    """Verify Gmail API configuration"""
    issues = []

    # Check for required environment variables
    required_vars = ['GMAIL_CLIENT_ID', 'GMAIL_CLIENT_SECRET']
    for var in required_vars:
        if not os.getenv(var):
            issues.append(f"Missing environment variable: {var}")

    # Check for credentials file
    if not os.path.exists('gmail-credentials.json'):
        issues.append("gmail-credentials.json file not found")

    return len(issues) == 0, issues


def verify_whatsapp_config() -> Tuple[bool, List[str]]:
    """Verify WhatsApp Web configuration"""
    issues = []

    # Check for session directory
    if not os.path.exists('sessions'):
        issues.append("sessions directory not found")

    # Check for required environment variables
    if not os.getenv('WHATSAPP_HEADLESS_MODE'):
        issues.append("WHATSAPP_HEADLESS_MODE not set in environment")

    return len(issues) == 0, issues


def verify_banking_config() -> Tuple[bool, List[str]]:
    """Verify banking API configuration"""
    issues = []

    # Check for required environment variables
    required_vars = ['BANKING_API_KEY', 'BANKING_API_BASE_URL']
    for var in required_vars:
        if not os.getenv(var):
            issues.append(f"Missing environment variable: {var}")

    return len(issues) == 0, issues


def verify_external_services() -> Dict[str, Dict[str, any]]:
    """Verify all external service configurations"""
    results = {}

    # Verify Gmail
    gmail_valid, gmail_issues = verify_gmail_config()
    results['gmail'] = {
        'valid': gmail_valid,
        'issues': gmail_issues,
        'configured': os.getenv('GMAIL_CLIENT_ID') is not None
    }

    # Verify WhatsApp
    whatsapp_valid, whatsapp_issues = verify_whatsapp_config()
    results['whatsapp'] = {
        'valid': whatsapp_valid,
        'issues': whatsapp_issues,
        'configured': os.path.exists('sessions') or os.getenv('WHATSAPP_HEADLESS_MODE')
    }

    # Verify Banking
    banking_valid, banking_issues = verify_banking_config()
    results['banking'] = {
        'valid': banking_valid,
        'issues': banking_issues,
        'configured': os.getenv('BANKING_API_KEY') is not None
    }

    return results


def main():
    """Main function to run external service verification"""
    print("Verifying external service configurations...")
    print("=" * 50)

    results = verify_external_services()

    for service, data in results.items():
        status = "✓" if data['valid'] else "✗"
        configured = "Yes" if data['configured'] else "No"
        print(f"\n{service.upper()}: {status} (Configured: {configured})")

        if data['issues']:
            for issue in data['issues']:
                print(f"  • {issue}")
        elif data['valid']:
            print("  • All checks passed")
        else:
            print("  • Configuration incomplete")

    # Overall summary
    print("\n" + "=" * 50)
    all_valid = all(data['valid'] for data in results.values())
    any_configured = any(data['configured'] for data in results.values())

    print(f"All Services Valid: {'✓ PASS' if all_valid else '✗ NEEDS CONFIGURATION'}")
    print(f"Any Services Configured: {'✓ YES' if any_configured else '✗ NONE'}")

    if all_valid and any_configured:
        print("\n🎉 External services are properly configured!")
        return 0
    else:
        print("\n⚠️  Some services need configuration before they can be used.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
EOF

echo "✓ Created external service verification script"

# Make the verification script executable
chmod +x setup-scripts/verify-external-services.py

# Create rate limiting configuration
cat > config/rate-limiting.json << 'EOF'
{
  "services": {
    "gmail": {
      "requests_per_minute": 10,
      "burst_capacity": 20,
      "cooldown_period": 60
    },
    "whatsapp": {
      "requests_per_minute": 30,
      "burst_capacity": 60,
      "cooldown_period": 30
    },
    "banking": {
      "requests_per_minute": 5,
      "burst_capacity": 10,
      "cooldown_period": 300
    }
  },
  "global": {
    "max_concurrent_requests": 10,
    "default_timeout": 30,
    "retry_attempts": 3,
    "backoff_multiplier": 2
  }
}
EOF

echo "✓ Created rate limiting configuration"

echo "External service access configuration completed!"
echo ""
echo "Configuration files created:"
echo "- config/external-services.json"
echo "- config/rate-limiting.json"
echo "- docs/gmail-api-setup.md"
echo "- docs/whatsapp-web-setup.md"
echo "- docs/banking-api-setup.md"
echo "- setup-scripts/verify-external-services.py"