#!/bin/bash

# Security Configuration Verification Script for Personal AI Employee Hackathon 0 Foundation

echo "Verifying security configuration..."

# Check that .env exists
if [ -f ".env" ]; then
    echo "✓ .env file exists"
else
    echo "✗ .env file does not exist"
    exit 1
fi

# Check that .env is in .gitignore
if grep -q ".env" .gitignore; then
    echo "✓ .env is in .gitignore"
else
    echo "✗ .env is not in .gitignore"
    exit 1
fi

# Check that sensitive directories are in .gitignore
SENSITIVE_DIRS=(".mcp" ".obsidian" "secrets/" "credentials/")
for dir in "${SENSITIVE_DIRS[@]}"; do
    if grep -q "$dir" .gitignore; then
        echo "✓ $dir is in .gitignore"
    else
        echo "⚠ $dir is not in .gitignore"
    fi
done

# Check that credential-related files are in .gitignore
CRED_FILES=(".env" "*.key" "*.pem" "*.crt" "config.json")
for file in "${CRED_FILES[@]}"; do
    if grep -q "$file" .gitignore; then
        echo "✓ $file pattern is in .gitignore"
    else
        echo "⚠ $file pattern is not in .gitignore"
    fi
done

# Check that security documentation exists
if [ -f "docs/security-best-practices.md" ]; then
    echo "✓ Security best practices documentation exists"
else
    echo "✗ Security best practices documentation missing"
fi

if [ -f "docs/credential-rotation.md" ]; then
    echo "✓ Credential rotation documentation exists"
else
    echo "✗ Credential rotation documentation missing"
fi

# Run the credential validation script
echo "Running credential validation..."
python3 setup-scripts/validate-credentials.py

echo "Security configuration verification completed!"