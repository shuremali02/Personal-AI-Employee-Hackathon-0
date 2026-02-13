#!/usr/bin/env python3
"""
Setup verification script for Personal AI Employee Hackathon 0
Verifies that all required components are installed and functional
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python 3.13+ is installed"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 13:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"✗ Python requirement not met. Found {version.major}.{version.minor}, need 3.13+")
        return False

def check_node_version():
    """Check if Node.js v24+ LTS is installed"""
    print("Checking Node.js version...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
        version_str = result.stdout.strip().replace('v', '')
        version = tuple(map(int, version_str.split('.')))

        if version[0] >= 24:
            print(f"✓ Node.js {result.stdout.strip()} detected")
            return True
        else:
            print(f"✗ Node.js requirement not met. Found v{version[0]}, need v24+")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Node.js not found")
        return False

def check_claude_code():
    """Check if Claude Code is installed"""
    print("Checking Claude Code installation...")
    try:
        result = subprocess.run(['claude', '--version'], capture_output=True, text=True, check=True)
        print(f"✓ Claude Code {result.stdout.strip()} detected")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Claude Code not found")
        return False

def check_uv():
    """Check if uv is installed"""
    print("Checking uv installation...")
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True, check=True)
        print(f"✓ uv {result.stdout.strip()} detected")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ uv not found")
        return False

def verify_project_structure():
    """Verify that project structure is properly set up"""
    print("Checking project structure...")

    required_dirs = [
        'setup-scripts',
        '.mcp',
        '.obsidian',
        'AI_Employee_Vault',
        'AI_Employee_Vault/Inbox',
        'AI_Employee_Vault/Needs_Action',
        'AI_Employee_Vault/Done',
        'src',
        'src/brain',
        'src/memory',
        'src/senses',
        'src/hands',
        'src/utils'
    ]

    required_files = [
        '.env',
        'README.md',
        'pyproject.toml',
        'AI_Employee_Vault/Dashboard.md',
        'AI_Employee_Vault/Company_Handbook.md',
        '.mcp/config.json'
    ]

    all_good = True

    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"✗ Missing directory: {directory}")
            all_good = False
        else:
            print(f"✓ Directory exists: {directory}")

    for file in required_files:
        if not Path(file).exists():
            print(f"✗ Missing file: {file}")
            all_good = False
        else:
            print(f"✓ File exists: {file}")

    return all_good

def main():
    print("="*60)
    print("Personal AI Employee - Foundation Setup Verification")
    print("="*60)

    checks = [
        ("Python 3.13+ Check", check_python_version),
        ("Node.js v24+ Check", check_node_version),
        ("Claude Code Check", check_claude_code),
        ("uv Check", check_uv),
        ("Project Structure Check", verify_project_structure)
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        result = check_func()
        results.append((name, result))

    print("\n" + "="*60)
    print("VERIFICATION SUMMARY:")
    print("="*60)

    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False

    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED! Foundation setup is complete.")
        print("\nNext steps:")
        print("1. Fill in your credentials in the .env file")
        print("2. Review the configuration files in .mcp/")
        print("3. Start building your AI employee capabilities!")
    else:
        print("❌ SOME CHECKS FAILED. Please address the issues above.")
        print("Some components may need manual installation or configuration.")
    print("="*60)

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())