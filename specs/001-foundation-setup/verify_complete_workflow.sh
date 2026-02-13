#!/bin/bash

# Comprehensive Setup Verification Script for Personal AI Employee Hackathon 0 Foundation

echo "=== Comprehensive Foundation Setup Verification ==="
echo ""

# Test complete workflow from development environment to external service access
echo "1. Testing Development Environment..."
bash setup-scripts/verify-setup.sh
echo ""

echo "2. Testing Security Configuration..."
bash setup-scripts/verify-security.sh
echo ""

echo "3. Testing Obsidian Vault Configuration..."
if [ -d "AI_Employee_Vault" ]; then
    echo "   ✓ Obsidian vault directory exists"
    # Check for required subdirectories
    if [ -d "AI_Employee_Vault/Inbox" ] && [ -d "AI_Employee_Vault/Needs_Action" ] && [ -d "AI_Employee_Vault/Done" ]; then
        echo "   ✓ All required vault directories exist"
    else
        echo "   ✗ Missing vault subdirectories"
    fi

    # Check for required files
    if [ -f "AI_Employee_Vault/Dashboard.md" ] && [ -f "AI_Employee_Vault/Company_Handbook.md" ]; then
        echo "   ✓ Required vault files exist"
    else
        echo "   ✗ Missing required vault files"
    fi
else
    echo "   ✗ Obsidian vault directory does not exist"
fi
echo ""

echo "4. Testing MCP Server Configuration..."
if [ -d ".mcp" ]; then
    echo "   ✓ .mcp directory exists"
    if [ -f ".mcp/config.json" ]; then
        echo "   ✓ MCP configuration file exists"
    else
        echo "   ✗ MCP configuration file missing"
    fi

    if [ -f ".mcp/start-servers.sh" ]; then
        echo "   ✓ MCP startup script exists"
    else
        echo "   ✗ MCP startup script missing"
    fi

    # Check server directories
    if [ -d ".mcp/servers/filesystem-mcp" ] && [ -d ".mcp/servers/email-mcp" ] && [ -d ".mcp/servers/browser-mcp" ]; then
        echo "   ✓ All MCP server directories exist"
    else
        echo "   ✗ Missing MCP server directories"
    fi
else
    echo "   ✗ .mcp directory does not exist"
fi
echo ""

echo "5. Testing External Service Configuration..."
if [ -f "config/external-services.json" ]; then
    echo "   ✓ External service configuration file exists"
else
    echo "   ✗ External service configuration file missing"
fi

if [ -f "config/rate-limiting.json" ]; then
    echo "   ✓ Rate limiting configuration exists"
else
    echo "   ✗ Rate limiting configuration missing"
fi

if [ -f "setup-scripts/verify-external-services.py" ]; then
    echo "   ✓ External service verification script exists"
else
    echo "   ✗ External service verification script missing"
fi
echo ""

echo "6. Testing Documentation..."
DOCS_CHECKED=0
DOCS_EXIST=0

DOC_FILES=(
    "docs/security-best-practices.md"
    "docs/credential-rotation.md"
    "docs/credential-security-audit.md"
    "docs/gmail-api-setup.md"
    "docs/whatsapp-web-setup.md"
    "docs/banking-api-setup.md"
    "docs/troubleshooting.md"
    "docs/quick-reference.md"
    "docs/backup-recovery.md"
    "docs/next-steps-bronze-tier.md"
    "docs/setup-completion-report.md"
)

for doc in "${DOC_FILES[@]}"; do
    ((DOCS_CHECKED++))
    if [ -f "$doc" ]; then
        ((DOCS_EXIST++))
        echo "   ✓ $doc exists"
    else
        echo "   ✗ $doc missing"
    fi
done

echo "   $DOCS_EXIST out of $DOCS_CHECKED documentation files exist"
echo ""

echo "7. Testing Setup Scripts..."
SCRIPTS_CHECKED=0
SCRIPTS_EXIST=0

SCRIPT_FILES=(
    "setup-scripts/verify-setup.sh"
    "setup-scripts/configure-security.sh"
    "setup-scripts/configure-vault.sh"
    "setup-scripts/setup-mcp-servers.sh"
    "setup-scripts/configure-external-services.sh"
    "setup-scripts/validate-credentials.py"
    "setup-scripts/verify-security.sh"
    "setup-scripts/test-credential-exposure.sh"
    "setup-scripts/verify-external-services.py"
)

for script in "${SCRIPT_FILES[@]}"; do
    ((SCRIPTS_CHECKED++))
    if [ -f "$script" ]; then
        ((SCRIPTS_EXIST++))
        echo "   ✓ $script exists"
    else
        echo "   ✗ $script missing"
    fi
done

echo "   $SCRIPTS_EXIST out of $SCRIPTS_CHECKED setup scripts exist"
echo ""

# Run the external service verification
echo "8. Running external service verification..."
python3 setup-scripts/verify-external-services.py
echo ""

# Final summary
echo "=== Final Verification Summary ==="
TOTAL_TASKS=77
COMPLETED_TASKS=$(grep -c "\- \[X\]" specs/001-foundation-setup/tasks.md)
PENDING_TASKS=$((TOTAL_TASKS - COMPLETED_TASKS))

echo "Total Tasks: $TOTAL_TASKS"
echo "Completed: $COMPLETED_TASKS"
echo "Pending: $PENDING_TASKS"
echo ""

if [ $PENDING_TASKS -eq 0 ]; then
    echo "🎉 All foundation setup tasks are complete!"
    echo "✅ Foundation setup verification: SUCCESS"
else
    echo "⚠️  $PENDING_TASKS tasks remain pending"
    echo "❌ Foundation setup verification: INCOMPLETE"
fi

echo ""
echo "Next steps:"
echo "- Review the setup-completion-report.md for final status"
echo "- Begin Bronze tier implementation as outlined in next-steps-bronze-tier.md"
echo "- Ensure all security measures are properly implemented before proceeding"