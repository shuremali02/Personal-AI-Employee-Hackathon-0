#!/usr/bin/env python3
"""
Security Measures Verification Script for Personal AI Employee

This script verifies that all security measures are in place and functioning
properly as part of the foundation setup.
"""

import os
import sys
import stat
from typing import Dict, List, Tuple

def check_file_permissions() -> Tuple[bool, List[str]]:
    """Check that sensitive files have appropriate permissions"""
    issues = []

    # Check .env file permissions (should not be readable by others)
    if os.path.exists('.env'):
        env_stat = os.stat('.env')
        if env_stat.st_mode & stat.S_IROTH:  # Others have read permission
            issues.append(".env file has read permissions for 'others' - should be restricted")
        if env_stat.st_mode & stat.S_IWOTH:  # Others have write permission
            issues.append(".env file has write permissions for 'others' - should be restricted")
    else:
        issues.append(".env file does not exist")

    return len(issues) == 0, issues

def check_sensitive_files_in_gitignore() -> Tuple[bool, List[str]]:
    """Check that sensitive files are in .gitignore"""
    issues = []

    if not os.path.exists('.gitignore'):
        issues.append(".gitignore file does not exist")
        return False, issues

    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()

    # List of sensitive patterns that should be ignored
    sensitive_patterns = [
        '.env',
        '*.env',
        '*.key',
        '*.pem',
        '*.crt',
        '*.cert',
        'secrets/',
        'credentials/',
        'config.json',  # If it contains credentials
        'tokens.json',
        'keys.json',
        'private/'
    ]

    for pattern in sensitive_patterns:
        if pattern not in gitignore_content:
            issues.append(f"Sensitive pattern '{pattern}' is not in .gitignore")

    return len(issues) == 0, issues

def check_directory_protection() -> Tuple[bool, List[str]]:
    """Check that sensitive directories have appropriate protection"""
    issues = []

    # Check for sensitive directories that should exist but be properly configured
    sensitive_dirs = ['.mcp', 'secrets', 'credentials', 'private']

    for directory in sensitive_dirs:
        if os.path.exists(directory):
            # Check if directory is in .gitignore
            if os.path.exists('.gitignore'):
                with open('.gitignore', 'r') as f:
                    gitignore_content = f.read()
                    if directory not in gitignore_content and directory + '/' not in gitignore_content:
                        issues.append(f"Sensitive directory '{directory}' is not in .gitignore")

    return len(issues) == 0, issues

def check_hardcoded_credentials() -> Tuple[bool, List[str]]:
    """Check for potential hardcoded credentials in code files"""
    issues = []

    # Extensions to scan for potential hardcoded credentials
    code_extensions = ['.py', '.js', '.ts', '.json', '.yaml', '.yml', '.sh', '.env']

    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in ['.git', '.mcp', 'node_modules', '__pycache__', '.pytest_cache']]

        for file in files:
            # Only check files with code extensions and exclude .env files
            if any(file.lower().endswith(ext) for ext in code_extensions) and not file.startswith('.env'):
                filepath = os.path.join(root, file)

                # Skip binary files
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    continue  # Skip binary files

                # Look for potential hardcoded credentials
                potential_creds = [
                    'password=', 'password:', 'secret=', 'secret:', 'token=', 'token:',
                    'key=', 'key:', 'api_key=', 'api_key:', 'client_secret=', 'client_secret:',
                    'access_token=', 'access_token:', 'bearer ', 'Authorization:'
                ]

                for cred in potential_creds:
                    if cred.lower() in content.lower() and ('http' not in cred.lower() or 'authorization' in cred.lower()):
                        # Check if it's just a variable declaration or actual value assignment
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if cred.lower() in line.lower():
                                # Check if there's an actual value (not just a declaration)
                                parts = line.split(cred.split('=')[0] if '=' in cred else cred.split(':')[0])
                                if len(parts) > 1 and len(parts[1].strip()) > 0 and not parts[1].strip().startswith('#') and not parts[1].strip().startswith('//'):
                                    issues.append(f"Potential hardcoded credential found in {filepath}:{i+1}")

    return len(issues) == 0, issues

def check_environment_configuration() -> Tuple[bool, List[str]]:
    """Check that environment is configured securely"""
    issues = []

    # Check that sensitive environment variables are not set in the current environment
    sensitive_env_vars = [
        'PASSWORD', 'SECRET', 'TOKEN', 'KEY', 'API_KEY', 'CLIENT_SECRET',
        'ACCESS_TOKEN', 'AUTH_TOKEN', 'SESSION_TOKEN'
    ]

    for var in sensitive_env_vars:
        if var in os.environ:
            issues.append(f"Sensitive environment variable '{var}' is set in the current environment")

    return len(issues) == 0, issues

def verify_all_security_measures() -> Dict[str, Tuple[bool, List[str]]]:
    """Run all security verifications"""
    results = {
        'file_permissions': check_file_permissions(),
        'gitignore_protection': check_sensitive_files_in_gitignore(),
        'directory_protection': check_directory_protection(),
        'hardcoded_credentials': check_hardcoded_credentials(),
        'environment_configuration': check_environment_configuration()
    }

    return results

def main():
    """Main function to run security verification"""
    print("Verifying security measures for Personal AI Employee Foundation Setup...")
    print("=" * 80)

    results = verify_all_security_measures()

    print("\nSecurity Measure Verification Results:")

    all_passed = True
    for check_name, (passed, issues) in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\n{check_name.replace('_', ' ').upper()}: {status}")

        if issues:
            all_passed = False
            for issue in issues:
                print(f"  • {issue}")
        elif passed:
            print("  • All checks passed")

    # Summary
    print(f"\nSUMMARY:")
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result[0])
    print(f"  Total Security Checks: {total_checks}")
    print(f"  Passed: {passed_checks}")
    print(f"  Failed: {total_checks - passed_checks}")

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL SECURITY MEASURES VERIFIED!")
        print("Foundation setup has appropriate security measures in place.")
        return 0
    else:
        print("❌ SOME SECURITY MEASURES NEED ATTENTION")
        print("Review the security issues above and address them before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())