#!/bin/bash

# Personal AI Employee - Foundation Setup Script
# This script installs all necessary dependencies for the foundation setup

set -e  # Exit on any error

echo "🚀 Installing Personal AI Employee Foundation Dependencies..."

# Check if Python 3.13+ is available
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [ $PYTHON_MAJOR -ge 3 ] && [ $PYTHON_MINOR -ge 13 ]; then
        echo "✅ Python $PYTHON_VERSION detected (3.13+)"
        PYTHON_CMD="python3"
    else
        echo "❌ Python requirement not met. Found $PYTHON_VERSION, need 3.13+"
        exit 1
    fi
else
    echo "❌ Python3 not found"
    exit 1
fi

# Check if Node.js 24+ is available
echo "Checking Node.js version..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | sed 's/v//')
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)

    if [ $NODE_MAJOR -ge 24 ]; then
        echo "✅ Node.js $NODE_VERSION detected (v24+)"
    else
        echo "❌ Node.js requirement not met. Found v$NODE_VERSION, need v24+"
        exit 1
    fi
else
    echo "❌ Node.js not found"
    exit 1
fi

# Check if Claude Code is available
echo "Checking Claude Code installation..."
if command -v claude &> /dev/null; then
    CLAUDE_VERSION=$(claude --version 2>&1)
    echo "✅ Claude Code $CLAUDE_VERSION detected"
else
    echo "⚠️  Claude Code not found (this may be intentional if you're using Claude Code Router)"
fi

# Check if uv is available
echo "Checking uv installation..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    echo "✅ uv $UV_VERSION detected"
else
    echo "Installing uv..."
    pip install uv
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version)
        echo "✅ uv $UV_VERSION installed"
    else
        echo "❌ Failed to install uv"
        exit 1
    fi
fi

# Install Python dependencies
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    uv pip install -r requirements.txt
    echo "✅ Python dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping Python dependencies"
fi

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    npm install
    echo "✅ Node.js dependencies installed"
else
    echo "⚠️  package.json not found, skipping Node.js dependencies"
fi

# Create necessary directories if they don't exist
echo "Creating project directories..."
mkdir -p AI_Employee_Vault/Inbox
mkdir -p AI_Employee_Vault/Needs_Action
mkdir -p AI_Employee_Vault/Done
mkdir -p .mcp/servers/email-mcp
mkdir -p .mcp/servers/browser-mcp
mkdir -p .mcp/servers/filesystem-mcp
mkdir -p src/brain
mkdir -p src/memory
mkdir -p src/senses
mkdir -p src/hands
mkdir -p src/utils

echo "✅ Project directories created"

# Create placeholder files if they don't exist
echo "Creating placeholder files..."

if [ ! -f "AI_Employee_Vault/Dashboard.md" ]; then
    echo "# AI Employee Dashboard

Welcome to your Personal AI Employee!

## Status
- System: Operational
- Last Check: $(date)

## Tasks
- [ ] Initialize system
- [ ] Configure watchers
- [ ] Set up MCP servers

" > AI_Employee_Vault/Dashboard.md
    echo "✅ Dashboard.md created"
fi

if [ ! -f "AI_Employee_Vault/Company_Handbook.md" ]; then
    echo "# Company Handbook

## Rules of Engagement
1. Always ask for approval before taking actions
2. Log all activities for audit purposes
3. Protect sensitive information
4. Operate within defined boundaries

## Contact Information
- Primary: [Your Name]
- Backup: [Backup Contact]

" > AI_Employee_Vault/Company_Handbook.md
    echo "✅ Company_Handbook.md created"
fi

if [ ! -f ".env" ]; then
    echo "# Personal AI Employee - Environment Variables
# DO NOT COMMIT THIS FILE TO VERSION CONTROL

# Claude Code Configuration
CLAUDE_API_KEY=

# Email Configuration
EMAIL_USERNAME=
EMAIL_PASSWORD=
EMAIL_IMAP_SERVER=
EMAIL_SMTP_SERVER=

# Other API Keys as needed
" > .env
    echo "✅ .env template created (remember to add to .gitignore)"
fi

if [ ! -f ".mcp/config.json" ]; then
    mkdir -p .mcp
    echo '{
  "servers": {
    "filesystem": {
      "enabled": true,
      "port": 8081
    },
    "email": {
      "enabled": false,
      "port": 8082
    },
    "browser": {
      "enabled": false,
      "port": 8083
    }
  }
}' > .mcp/config.json
    echo "✅ MCP config created"
fi

echo "✅ Placeholder files created"

# Verify gitignore has sensitive files
echo "Checking .gitignore configuration..."
if [ -f ".gitignore" ]; then
    if ! grep -q ".env" .gitignore; then
        echo ".env" >> .gitignore
        echo "✅ Added .env to .gitignore"
    fi
    if ! grep -q "AI_Employee_Vault/" .gitignore; then
        echo "AI_Employee_Vault/" >> .gitignore
        echo "⚠️  Added AI_Employee_Vault/ to .gitignore (you may want to track specific files)"
    fi
else
    echo "# Personal AI Employee - Git Ignore
.env
*.env
.env.local
.env.*.local
AI_Employee_Vault/
.mcp/sessions/
*.log
node_modules/
__pycache__/
*.pyc
" > .gitignore
    echo "✅ Created .gitignore with sensitive files excluded"
fi

echo ""
echo "🎉 Foundation setup installation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Fill in your credentials in the .env file"
echo "2. Review the configuration files in .mcp/"
echo "3. Follow the tasks in specs/001-foundation-setup/tasks.md"
echo "4. Run verification: python specs/001-foundation-setup/verify_setup.py"
echo ""
echo "💡 Tip: Start with User Story 1 (Development Environment Setup) as your MVP"