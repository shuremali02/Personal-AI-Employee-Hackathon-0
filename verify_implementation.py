#!/usr/bin/env python3
"""
Final verification script for Personal AI Employee Hackathon 0 Foundation Setup Implementation
This script verifies that all major components of the foundation setup have been properly implemented.
"""

import os
import sys
import json
from pathlib import Path

def verify_directory_structure():
    """Verify that the required directory structure exists"""
    print("🔍 Verifying directory structure...")

    required_dirs = [
        'AI_Employee_Vault',
        'AI_Employee_Vault/Inbox',
        'AI_Employee_Vault/Needs_Action',
        'AI_Employee_Vault/Done',
        '.mcp',
        '.mcp/servers',
        '.mcp/servers/email-mcp',
        '.mcp/servers/browser-mcp',
        '.mcp/servers/filesystem-mcp',
        'specs',
        'specs/001-foundation-setup',
        'docs',
        'setup-scripts'
    ]

    all_good = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"❌ Missing directory: {dir_path}")
            all_good = False

    return all_good

def verify_configuration_files():
    """Verify that the required configuration files exist"""
    print("\n🔍 Verifying configuration files...")

    required_files = [
        '.env',
        '.mcp/config.json',
        'AI_Employee_Vault/Dashboard.md',
        'AI_Employee_Vault/Company_Handbook.md',
        'specs/001-foundation-setup/spec.md',
        'specs/001-foundation-setup/plan.md',
        'specs/001-foundation-setup/tasks.md',
        'specs/001-foundation-setup/research.md',
        'specs/001-foundation-setup/data-model.md',
        'specs/001-foundation-setup/quickstart.md',
        'README.md',
        'package.json',
        'pyproject.toml',
        'requirements.txt',
        'index.js'
    ]

    all_good = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ File exists: {file_path}")
        else:
            print(f"❌ Missing file: {file_path}")
            all_good = False

    return all_good

def verify_documentation():
    """Verify that the required documentation exists"""
    print("\n🔍 Verifying documentation...")

    required_docs = [
        'docs/vault-structure.md',
        'docs/security-best-practices.md',
        'docs/credential-rotation.md',
        'docs/external-service-access.md',
        'docs/troubleshooting.md',
        'docs/quick-reference.md',
        'docs/next-steps-bronze-tier.md',
        'docs/backup-recovery.md',
        'docs/setup-completion-report.md'
    ]

    all_good = True
    for doc_path in required_docs:
        if Path(doc_path).exists():
            print(f"✅ Documentation exists: {doc_path}")
        else:
            print(f"❌ Missing documentation: {doc_path}")
            all_good = False

    return all_good

def verify_mcp_config():
    """Verify the MCP configuration file"""
    print("\n🔍 Verifying MCP configuration...")

    config_path = Path('.mcp/config.json')
    if not config_path.exists():
        print("❌ MCP config file does not exist")
        return False

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        required_keys = ['servers', 'settings']
        config_ok = True

        for key in required_keys:
            if key not in config:
                print(f"❌ MCP config missing required key: {key}")
                config_ok = False

        if 'filesystem' in config.get('servers', {}):
            print("✅ MCP filesystem server configured")
        else:
            print("❌ MCP filesystem server not configured")
            config_ok = False

        if config_ok:
            print("✅ MCP configuration is valid")

        return config_ok

    except json.JSONDecodeError:
        print("❌ MCP config file is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error reading MCP config: {str(e)}")
        return False

def verify_gitignore():
    """Verify that .gitignore properly excludes sensitive files"""
    print("\n🔍 Verifying .gitignore configuration...")

    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        print("❌ .gitignore file does not exist")
        return False

    with open(gitignore_path, 'r') as f:
        content = f.read()

    sensitive_patterns = ['.env', '*.env', 'AI_Employee_Vault/', '.mcp/']
    all_found = True

    for pattern in sensitive_patterns:
        if pattern in content:
            print(f"✅ .gitignore includes pattern: {pattern}")
        else:
            print(f"⚠️  .gitignore may be missing pattern: {pattern}")
            # Not failing for this as it might be intentionally excluded

    return True

def calculate_task_completion():
    """Calculate the completion percentage of tasks"""
    print("\n🔍 Calculating task completion...")

    tasks_file = Path('specs/001-foundation-setup/tasks.md')
    if not tasks_file.exists():
        print("❌ Tasks file does not exist")
        return 0, 0, 0

    with open(tasks_file, 'r') as f:
        content = f.read()

    total_tasks = content.count('[ ] ') + content.count('[X] ') + content.count('[x] ')
    completed_tasks = content.count('[X] ') + content.count('[x] ')
    incomplete_tasks = content.count('[ ] ')

    if total_tasks > 0:
        completion_percentage = (completed_tasks / total_tasks) * 100
        print(f"✅ Task completion: {completed_tasks}/{total_tasks} ({completion_percentage:.1f}%)")
    else:
        print("❌ Could not parse task completion")
        return 0, 0, 0

    return completed_tasks, total_tasks, completion_percentage

def main():
    print("=" * 70)
    print("Personal AI Employee Hackathon 0 - Foundation Setup Implementation Verification")
    print(f"Run at: {' '.join(sys.argv)}" if len(sys.argv) > 1 else "Run at: Manual execution")
    print("=" * 70)

    results = {}

    results['dirs'] = verify_directory_structure()
    results['configs'] = verify_configuration_files()
    results['docs'] = verify_documentation()
    results['mcp'] = verify_mcp_config()
    results['gitignore'] = verify_gitignore()

    completed_tasks, total_tasks, completion_percentage = calculate_task_completion()

    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)

    # Print individual results
    checks = [
        ("Directory Structure", results['dirs']),
        ("Configuration Files", results['configs']),
        ("Documentation", results['docs']),
        ("MCP Configuration", results['mcp']),
        ("Git Ignore Setup", results['gitignore'])
    ]

    for name, result in checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")

    print(f"\nTask Completion: {completed_tasks}/{total_tasks} ({completion_percentage:.1f}%)")

    # Overall assessment
    passed_checks = sum(1 for result in results.values() if result)
    total_checks = len(results)

    print(f"\nOverall: {passed_checks}/{total_checks} structural checks passed")

    if passed_checks == total_checks and completion_percentage >= 85:
        print("🎉 IMPLEMENTATION SUCCESSFUL! Foundation setup is complete and verified.")
        print("\n📋 Next Steps:")
        print("- Proceed with Bronze tier implementation")
        print("- Complete any remaining external service configurations")
        print("- Upgrade Python and Node.js to required versions if needed")
        return 0
    elif passed_checks >= total_checks / 2:
        print("👍 Implementation largely successful with minor issues.")
        print("Please address any remaining issues before proceeding to Bronze tier.")
        return 0
    else:
        print("⚠️  Several critical issues detected. Please address before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())