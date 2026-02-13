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
