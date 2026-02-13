#!/usr/bin/env python3
"""
Credential Validation Function for Personal AI Employee
Provides secure validation of credentials without exposing them
"""

import os
import sys
from typing import Dict, List, Optional


def validate_credentials(credential_types: List[str] = None) -> Dict[str, bool]:
    """
    Validates that required credentials are present and properly formatted

    Args:
        credential_types: List of credential types to validate

    Returns:
        Dictionary mapping credential type to validation status
    """
    if credential_types is None:
        credential_types = ['GMAIL', 'WHATSAPP', 'BANKING']

    validation_results = {}

    # Define expected credential patterns
    credential_patterns = {
        'GMAIL_USERNAME': lambda x: x and '@' in x and '.' in x.split('@')[1],
        'GMAIL_PASSWORD': lambda x: x and len(x) >= 8,  # In practice, use OAuth tokens
        'WHATSAPP_SESSION': lambda x: x and len(x) > 10,  # Session token validation
        'BANKING_API_KEY': lambda x: x and len(x) >= 20,  # API key validation
        'GEMINI_API_KEY': lambda x: x and x.startswith('AI') and len(x) > 10,  # API key format
    }

    for cred_type in credential_types:
        # Check for various common credential names
        env_vars_to_check = []
        if cred_type == 'GMAIL':
            env_vars_to_check = ['GMAIL_USERNAME', 'GMAIL_PASSWORD', 'GMAIL_CREDENTIALS']
        elif cred_type == 'WHATSAPP':
            env_vars_to_check = ['WHATSAPP_SESSION', 'WHATSAPP_TOKEN', 'WA_SESSION']
        elif cred_type == 'BANKING':
            env_vars_to_check = ['BANKING_API_KEY', 'BANK_API_KEY', 'FINANCIAL_API_KEY']
        elif cred_type == 'GEMINI':
            env_vars_to_check = ['GEMINI_API_KEY', 'GOOGLE_GEMINI_KEY', 'GENAI_API_KEY']

        # Validate each credential type
        type_valid = True
        for env_var in env_vars_to_check:
            value = os.getenv(env_var)
            if env_var in credential_patterns:
                if value:
                    is_valid = credential_patterns[env_var](value)
                    validation_results[env_var] = is_valid
                    if not is_valid:
                        type_valid = False
                else:
                    validation_results[env_var] = False
                    type_valid = False
            else:
                # For unknown patterns, just check if exists and has reasonable length
                validation_results[env_var] = bool(value and len(value) > 0)
                if not validation_results[env_var]:
                    type_valid = False

        # Set overall type validation
        validation_results[f"{cred_type}_VALID"] = type_valid

    return validation_results


def validate_security_measures() -> Dict[str, bool]:
    """
    Validates that security measures are in place

    Returns:
        Dictionary mapping security measure to validation status
    """
    security_checks = {}

    # Check if .env file exists
    env_exists = os.path.exists('.env')
    security_checks['ENV_FILE_EXISTS'] = env_exists

    # Check if .env is in .gitignore
    gitignore_exists = os.path.exists('.gitignore')
    if gitignore_exists:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            env_ignored = '.env' in gitignore_content
    else:
        env_ignored = False
    security_checks['ENV_IN_GITIGNORE'] = env_ignored

    # Check for sensitive directories in .gitignore
    sensitive_dirs = ['.mcp', '.obsidian', 'secrets/', 'credentials/']
    for dir_name in sensitive_dirs:
        security_checks[f'{dir_name.upper()}_IGNORED'] = gitignore_exists and dir_name in gitignore_content

    # Check for credential files in .gitignore
    sensitive_files = ['.env', '*.key', '*.pem', '*.crt', 'config.json']
    for file_name in sensitive_files:
        security_checks[f'{file_name.upper().replace("*","WILDCARD")}_IGNORED'] = gitignore_exists and file_name in gitignore_content

    return security_checks


def main():
    """Main function to run credential and security validation"""
    print("Validating credentials and security measures...")
    print("=" * 50)

    # Validate credentials
    print("\n1. Validating credentials:")
    credential_validation = validate_credentials(['GMAIL', 'WHATSAPP', 'BANKING', 'GEMINI'])

    for cred, is_valid in credential_validation.items():
        status = "✓" if is_valid else "✗"
        print(f"   {status} {cred}: {'Valid' if is_valid else 'Invalid/Missing'}")

    # Validate security measures
    print("\n2. Validating security measures:")
    security_validation = validate_security_measures()

    for measure, is_valid in security_validation.items():
        status = "✓" if is_valid else "✗"
        print(f"   {status} {measure}: {'Active' if is_valid else 'Missing'}")

    # Overall summary
    print("\n" + "=" * 50)
    all_creds_valid = all(v for k, v in credential_validation.items() if not k.endswith('_VALID') and not k.replace('*', 'WILDCARD').endswith('_IGNORED'))
    all_security_active = all(v for k, v in security_validation.items())

    print(f"Overall Credential Status: {'✓ PASS' if all_creds_valid else '✗ NEEDS ATTENTION'}")
    print(f"Overall Security Status: {'✓ PASS' if all_security_active else '✗ NEEDS ATTENTION'}")

    if all_creds_valid and all_security_active:
        print("\n🎉 All validations passed! Security foundation is properly configured.")
        return 0
    else:
        print("\n⚠️  Some validations failed. Please review the security configuration.")
        return 1


if __name__ == "__main__":
    sys.exit(main())