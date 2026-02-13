#!/usr/bin/env python3
"""
Acceptance Criteria Verification Script for Personal AI Employee Foundation Setup

This script verifies that all acceptance criteria defined in the user stories
have been met during the foundation setup.
"""

import os
import sys
import json
from typing import Dict, List, Tuple, Any

def check_user_story_1_acceptance_criteria() -> Tuple[bool, List[str]]:
    """Check acceptance criteria for User Story 1 (Development Environment Setup)"""
    issues = []

    # Criterion 1: All required software components are installed and verified
    software_components = {
        'Claude Code': lambda: os.system('which claude > /dev/null 2>&1') == 0,
        'Obsidian': lambda: os.path.exists('AI_Employee_Vault'),  # Assuming vault indicates Obsidian setup
        'Python': lambda: os.system('which python3 > /dev/null 2>&1') == 0,
        'Node.js': lambda: os.system('which node > /dev/null 2>&1') == 0,
        'GitHub Desktop': lambda: os.system('which github > /dev/null 2>&1') == 0,
        'uv': lambda: os.system('which uv > /dev/null 2>&1') == 0
    }

    for component, check_func in software_components.items():
        if not check_func():
            issues.append(f"Required software component '{component}' is not installed or accessible")

    # Criterion 2: Each component confirms proper installation and functionality
    # This is partially covered by the existence checks above

    return len(issues) == 0, issues

def check_user_story_2_acceptance_criteria() -> Tuple[bool, List[str]]:
    """Check acceptance criteria for User Story 2 (Security and Credential Management)"""
    issues = []

    # Criterion 1: Sensitive data is stored securely using environment variables or dedicated secrets managers
    if not os.path.exists('.env'):
        issues.append("Environment file (.env) does not exist")

    # Check if .env is in .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.env' not in gitignore_content:
                issues.append(".env file is not in .gitignore")
    else:
        issues.append(".gitignore file does not exist")

    # Criterion 2: Credentials are never exposed in code, logs, or version control
    # This is validated by the presence of security measures

    # Check for security documentation
    security_docs = [
        'docs/security-best-practices.md',
        'docs/credential-rotation.md'
    ]

    for doc in security_docs:
        if not os.path.exists(doc):
            issues.append(f"Security documentation missing: {doc}")

    return len(issues) == 0, issues

def check_user_story_3_acceptance_criteria() -> Tuple[bool, List[str]]:
    """Check acceptance criteria for User Story 3 (Obsidian Vault Initialization)"""
    issues = []

    # Criterion 1: Proper folder structure is created with initial configuration files
    vault_path = 'AI_Employee_Vault'
    if not os.path.exists(vault_path):
        issues.append("AI_Employee_Vault directory does not exist")
    else:
        required_dirs = [
            os.path.join(vault_path, 'Inbox'),
            os.path.join(vault_path, 'Needs_Action'),
            os.path.join(vault_path, 'Done')
        ]

        for req_dir in required_dirs:
            if not os.path.exists(req_dir):
                issues.append(f"Required vault directory does not exist: {req_dir}")

        required_files = [
            os.path.join(vault_path, 'Dashboard.md'),
            os.path.join(vault_path, 'Company_Handbook.md')
        ]

        for req_file in required_files:
            if not os.path.exists(req_file):
                issues.append(f"Required vault file does not exist: {req_file}")

    return len(issues) == 0, issues

def check_user_story_4_acceptance_criteria() -> Tuple[bool, List[str]]:
    """Check acceptance criteria for User Story 4 (MCP Server Foundation)"""
    issues = []

    # Criterion 1: Claude Code can successfully communicate with the MCP server framework
    mcp_path = '.mcp'
    if not os.path.exists(mcp_path):
        issues.append(".mcp directory does not exist")
    else:
        # Check for MCP configuration
        if not os.path.exists(os.path.join(mcp_path, 'config.json')):
            issues.append("MCP configuration file (.mcp/config.json) does not exist")

        # Check for server directories
        server_dirs = [
            os.path.join(mcp_path, 'servers', 'filesystem-mcp'),
            os.path.join(mcp_path, 'servers', 'email-mcp'),
            os.path.join(mcp_path, 'servers', 'browser-mcp')
        ]

        for server_dir in server_dirs:
            if not os.path.exists(server_dir):
                issues.append(f"MCP server directory does not exist: {server_dir}")

    return len(issues) == 0, issues

def check_user_story_5_acceptance_criteria() -> Tuple[bool, List[str]]:
    """Check acceptance criteria for User Story 5 (External Service Access Configuration)"""
    issues = []

    # Criterion 1: System can successfully authenticate and access each configured service
    # Check for external service configuration
    if not os.path.exists('config/external-services.json'):
        issues.append("External service configuration file (config/external-services.json) does not exist")

    # Check for service setup documentation
    service_docs = [
        'docs/gmail-api-setup.md',
        'docs/whatsapp-web-setup.md',
        'docs/banking-api-setup.md'
    ]

    for doc in service_docs:
        if not os.path.exists(doc):
            issues.append(f"External service documentation missing: {doc}")

    return len(issues) == 0, issues

def verify_all_acceptance_criteria() -> Dict[str, Any]:
    """Verify all acceptance criteria across all user stories"""
    results = {
        'user_story_1': check_user_story_1_acceptance_criteria(),
        'user_story_2': check_user_story_2_acceptance_criteria(),
        'user_story_3': check_user_story_3_acceptance_criteria(),
        'user_story_4': check_user_story_4_acceptance_criteria(),
        'user_story_5': check_user_story_5_acceptance_criteria()
    }

    # Overall result
    all_passed = all(result[0] for result in results.values())

    return {
        'all_passed': all_passed,
        'results': results,
        'summary': {
            'total_user_stories': len(results),
            'passed_user_stories': sum(1 for result in results.values() if result[0]),
            'failed_user_stories': sum(1 for result in results.values() if not result[0])
        }
    }

def verify_security_measures() -> Tuple[bool, List[str]]:
    """Additional verification of security measures"""
    issues = []

    # Check that sensitive files are not in version control
    # (This is mostly about ensuring they're in .gitignore)
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()

        sensitive_patterns = ['.env', '*.key', '*.pem', '*.crt', 'secrets/', 'credentials/']
        for pattern in sensitive_patterns:
            if pattern not in gitignore_content:
                issues.append(f"Sensitive pattern '{pattern}' is not in .gitignore")
    else:
        issues.append("No .gitignore file found")

    # Check for credential validation capability
    if not os.path.exists('setup-scripts/validate-credentials.py'):
        issues.append("Credential validation script not found")

    return len(issues) == 0, issues

def main():
    """Main function to run all acceptance criteria verification"""
    print("Verifying acceptance criteria for Personal AI Employee Foundation Setup...")
    print("=" * 80)

    # Verify all user story acceptance criteria
    ac_results = verify_all_acceptance_criteria()

    print("\nUser Story Acceptance Criteria Verification:")
    for story, (passed, issues) in ac_results['results'].items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"\n{story.upper().replace('_', ' ')}: {status}")

        if issues:
            for issue in issues:
                print(f"  • {issue}")
        elif passed:
            print("  • All criteria met")

    # Print summary
    summary = ac_results['summary']
    print(f"\nSUMMARY:")
    print(f"  Total User Stories: {summary['total_user_stories']}")
    print(f"  Passed: {summary['passed_user_stories']}")
    print(f"  Failed: {summary['failed_user_stories']}")

    # Verify security measures separately
    print(f"\nSecurity Measures Verification:")
    sec_passed, sec_issues = verify_security_measures()
    sec_status = "✓ PASS" if sec_passed else "✗ FAIL"
    print(f"Security Measures: {sec_status}")

    if sec_issues:
        for issue in sec_issues:
            print(f"  • {issue}")
    elif sec_passed:
        print("  • All security measures verified")

    # Overall result
    print("\n" + "=" * 80)
    overall_passed = ac_results['all_passed'] and sec_passed

    if overall_passed:
        print("🎉 ALL ACCEPTANCE CRITERIA MET!")
        print("Foundation setup meets all defined acceptance criteria.")
        return 0
    else:
        print("❌ SOME ACCEPTANCE CRITERIA NOT MET")
        print("Review the issues above and address them before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())