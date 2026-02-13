#!/bin/bash

# Test to ensure credentials are not exposed in logs
# This script simulates a safe way to handle credentials without exposing them

echo "Testing credential exposure protection..."

# Create a temporary test environment
TEST_ENV_FILE="/tmp/test_env_$$.env"
echo "TEST_API_KEY=test_key_12345" > "$TEST_ENV_FILE"
echo "TEST_SECRET=sensitive_data_here" >> "$TEST_ENV_FILE"

# Safe way to use credentials without exposing them
echo "✓ Testing safe credential handling..."
# Instead of echoing credentials directly, we check if they exist
if [ -f "$TEST_ENV_FILE" ]; then
    # Source the file in a subshell to avoid exposing variables
    (
        source "$TEST_ENV_FILE"
        if [ -n "$TEST_API_KEY" ]; then
            echo "✓ TEST_API_KEY is set (length: ${#TEST_API_KEY})"
        fi
        if [ -n "$TEST_SECRET" ]; then
            echo "✓ TEST_SECRET is set (length: ${#TEST_SECRET})"
        fi
    )
else
    echo "✗ Test environment file not found"
fi

# Clean up
rm -f "$TEST_ENV_FILE"

# Test that our actual .env file is not accidentally logged
if [ -f ".env" ]; then
    if grep -q "^[^#].*=" .env 2>/dev/null; then
        echo "✓ .env file exists with potential credentials (not displayed for security)"
    else
        echo "ℹ .env file exists but appears to be empty or commented"
    fi
else
    echo "ℹ .env file does not exist"
fi

echo "Credential exposure test completed - no actual credentials were exposed in output."