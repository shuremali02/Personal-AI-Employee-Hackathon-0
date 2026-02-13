#!/bin/bash

# Obsidian Vault Configuration Script for Personal AI Employee Hackathon 0 Foundation

echo "Configuring Obsidian vault settings..."

# Verify vault structure exists
VAULT_PATH="AI_Employee_Vault"
if [ ! -d "$VAULT_PATH" ]; then
    echo "Creating AI_Employee_Vault directory..."
    mkdir -p "$VAULT_PATH"
fi

# Create the required folder structure if not exists
mkdir -p "$VAULT_PATH/Inbox"
mkdir -p "$VAULT_PATH/Needs_Action"
mkdir -p "$VAULT_PATH/Done"

# Create basic configuration if not exists
if [ ! -d "$VAULT_PATH/.obsidian" ]; then
    mkdir -p "$VAULT_PATH/.obsidian"

    # Create basic Obsidian configuration
    cat > "$VAULT_PATH/.obsidian/workspace.json" << 'EOF'
{
  "main": {
    "id": "main-workspace",
    "type": "split",
    "children": [
      {
        "id": "main-content",
        "type": "tabs",
        "children": [
          {
            "id": "dashboard-tab",
            "type": "leaf",
            "pinned": true,
            "state": {
              "type": "markdown",
              "state": {
                "file": "Dashboard.md",
                "mode": "source"
              }
            }
          }
        ]
      }
    ],
    "direction": "vertical"
  },
  "left": {
    "id": "left-dock",
    "type": "split",
    "children": [
      {
        "id": "file-explorer",
        "type": "tabs",
        "children": [
          {
            "id": "explorer-tab",
            "type": "leaf",
            "state": {
              "type": "file-explorer",
              "state": {}
            }
          }
        ]
      }
    ],
    "direction": "horizontal",
    "width": 300
  }
}
EOF

    # Create core plugins configuration
    cat > "$VAULT_PATH/.obsidian/core-plugins.json" << 'EOF'
[
  "file-explorer",
  "global-search",
  "switcher",
  "graph",
  "backlink",
  "canvas",
  "outgoing-link",
  "tag-pane",
  "page-preview",
  "daily-notes",
  "templates",
  "note-composer",
  "command-palette",
  "editor-status",
  "bookmarks",
  "outline",
  "word-count",
  "file-recovery"
]
EOF

    # Create appearance configuration
    cat > "$VAULT_PATH/.obsidian/appearance.json" << 'EOF'
{
  "accentColor": "",
  "theme": "moonstone",
  "baseFontSize": 16,
  "showViewHeader": true
}
EOF

    echo "✓ Created basic Obsidian configuration"
fi

# Verify that Dashboard.md and Company_Handbook.md exist
if [ ! -f "$VAULT_PATH/Dashboard.md" ]; then
    cat > "$VAULT_PATH/Dashboard.md" << 'EOF'
# AI Employee Dashboard

## Inbox
- [[Inbox/]]

## Needs Action
- [[Needs_Action/]]

## Done
- [[Done/]]

## Quick Actions
- [ ] Check Gmail for new emails
- [ ] Review WhatsApp messages
- [ ] Monitor financial accounts
- [ ] Update task status

## Daily Summary
- Date: YYYY-MM-DD
- Tasks completed:
- Pending items:
- Issues encountered:

## Configuration
- MCP servers status: [Active/Inactive]
- External services status: [Connected/Disconnected]
- Security status: [Verified/Pending]
EOF
    echo "✓ Created Dashboard.md"
fi

if [ ! -f "$VAULT_PATH/Company_Handbook.md" ]; then
    cat > "$VAULT_PATH/Company_Handbook.md" << 'EOF'
# Company Handbook for AI Employee

## Mission Statement
The AI Employee serves as an autonomous assistant to handle routine tasks, monitor communications, and support business operations.

## Rules of Engagement
1. **Security First**: Never expose credentials or sensitive information
2. **Privacy**: Respect confidentiality of all communications
3. **Efficiency**: Prioritize high-impact tasks
4. **Reliability**: Maintain consistent monitoring and response
5. **Transparency**: Log all actions for accountability

## Operational Guidelines
### Priority Levels
- **Critical**: Immediate attention required (security issues, urgent communications)
- **High**: Address within 1 hour (important emails, time-sensitive tasks)
- **Medium**: Address within 4 hours (routine communications, scheduled tasks)
- **Low**: Address within 24 hours (non-urgent updates, informational content)

### Response Protocols
- Acknowledge receipt of important communications
- Escalate issues beyond defined scope
- Maintain professional tone in all interactions
- Follow up on pending items regularly

### Escalation Triggers
- Security breaches or suspicious activity
- Requests beyond authorized scope
- Technical failures preventing task completion
- Ambiguous instructions requiring human judgment

## Communication Templates
### Standard Response Template
```
Thank you for your message. This is an automated response from the AI Employee system.
[Specific action taken or status update]
[Next steps or expected timeline]
```

### Escalation Template
```
This request requires human intervention. Escalating to human operator.
Reason: [Specify reason]
Priority: [Critical/High/Medium/Low]
```

## Security Protocols
- Never share credentials or sensitive information
- Log all access to sensitive data
- Report suspicious activities immediately
- Follow credential rotation schedule
EOF
    echo "✓ Created Company_Handbook.md"
fi

echo "Obsidian vault configuration completed!"
echo ""
echo "Vault structure:"
echo "- AI_Employee_Vault/"
echo "  - Dashboard.md"
echo "  - Company_Handbook.md"
echo "  - Inbox/"
echo "  - Needs_Action/"
echo "  - Done/"
echo "  - .obsidian/ (configuration)"