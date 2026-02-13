#!/bin/bash

# Setup Verification Script for Personal AI Employee Hackathon 0 Foundation
# Verifies that all required components are properly installed

echo "=== Personal AI Employee Foundation Setup Verification ==="
echo ""

# Check Claude Code
echo "1. Checking Claude Code..."
if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>&1)
    echo "   ✓ Claude Code found: $CLAUDE_VERSION"
else
    echo "   ✗ Claude Code not found"
fi
echo ""

# Check Obsidian (check if command exists or if directory exists)
echo "2. Checking Obsidian..."
if [ -d "AI_Employee_Vault/.obsidian" ] || command -v obsidian &> /dev/null; then
    echo "   ✓ Obsidian vault directory exists or Obsidian command available"
else
    echo "   ⚠ Obsidian vault directory not found and no Obsidian command"
fi
echo ""

# Check Python
echo "3. Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "   ✓ Python found: $PYTHON_VERSION"

    # Extract major.minor version
    VERSION_NUM=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if (( $(echo "$VERSION_NUM >= 3.13" | bc -l) )); then
        echo "   ✓ Python version meets requirement (>= 3.13)"
    else
        echo "   ⚠ Python version is $VERSION_NUM (requirement: >= 3.13)"
    fi
else
    echo "   ✗ Python not found"
fi
echo ""

# Check Node.js
echo "4. Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version 2>&1)
    echo "   ✓ Node.js found: $NODE_VERSION"

    # Extract major version
    MAJOR_VERSION=$(node -v | sed 's/v\([0-9]*\).*/\1/')
    if [ "$MAJOR_VERSION" -ge 24 ]; then
        echo "   ✓ Node.js version meets requirement (>= 24)"
    else
        echo "   ⚠ Node.js version is $NODE_VERSION (requirement: >= v24)"
    fi
else
    echo "   ✗ Node.js not found"
fi
echo ""

# Check GitHub Desktop
echo "5. Checking GitHub Desktop..."
if command -v github &> /dev/null; then
    echo "   ✓ GitHub Desktop found"
else
    echo "   ⚠ GitHub Desktop command not found (may still be installed)"
fi
echo ""

# Check uv
echo "6. Checking uv..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version 2>&1)
    echo "   ✓ uv found: $UV_VERSION"
else
    echo "   ✗ uv not found"
fi
echo ""

# Check project structure
echo "7. Checking project structure..."
if [ -d "AI_Employee_Vault" ]; then
    echo "   ✓ AI_Employee_Vault directory exists"
else
    echo "   ✗ AI_Employee_Vault directory not found"
fi

if [ -d ".mcp" ]; then
    echo "   ✓ .mcp directory exists"
else
    echo "   ⚠ .mcp directory not found"
fi

if [ -f ".env" ]; then
    echo "   ✓ .env file exists"
else
    echo "   ⚠ .env file not found"
fi
echo ""

# Check setup scripts directory
echo "8. Checking setup scripts..."
if [ -d "setup-scripts" ]; then
    echo "   ✓ setup-scripts directory exists"
    SCRIPT_COUNT=$(ls setup-scripts/*.sh 2>/dev/null | wc -l)
    echo "   ✓ Found $SCRIPT_COUNT setup script(s)"
else
    echo "   ⚠ setup-scripts directory not found"
fi
echo ""

echo "=== Verification Complete ==="
echo ""
echo "Note: Some warnings may appear if certain components don't meet the exact version requirements."
echo "These can be addressed based on your specific needs and system constraints."