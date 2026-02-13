# Quick Reference Guide - Personal AI Employee Foundation Setup

## Overview
This guide provides quick access to common commands, configurations, and procedures for the Personal AI Employee Foundation Setup.

## Essential Commands

### System Status
- Check Claude Code: `claude --version`
- Check Python: `python3 --version`
- Check Node.js: `node --version`
- Check uv: `uv --version`

### MCP Server Management
- Start MCP servers: `claude mcp start`
- Check MCP status: `claude mcp status`
- Restart MCP servers: `claude mcp restart`
- MCP configuration: `.mcp/config.json`

### Vault Operations
- Check vault structure: `ls -la AI_Employee_Vault/`
- Dashboard file: `AI_Employee_Vault/Dashboard.md`
- Company handbook: `AI_Employee_Vault/Company_Handbook.md`

### Verification
- Run verification: `python specs/001-foundation-setup/verify_setup.py`
- Check all dependencies: `bash setup-scripts/install-dependencies.sh`

## Configuration Files

### Main Configuration Locations
- Environment variables: `.env`
- MCP configuration: `.mcp/config.json`
- Project dependencies: `requirements.txt`, `package.json`
- Git configuration: `.gitignore`

### Critical Settings
- Claude Code API key: `CLAUDE_API_KEY=***`
- Email settings: `EMAIL_*` variables
- MCP server ports: 8081-8083

## Security Essentials

### Credential Management
- Store all credentials in `.env` file
- Never commit `.env` to version control
- Use environment variables for sensitive data
- Regular credential rotation (monthly recommended)

### Access Control
- Human-in-the-loop for critical actions
- Approval required for financial operations
- Audit logging for all actions
- Local-first architecture (no cloud sync of sensitive data)

## Common Tasks

### Daily Operations
1. Check system health: Review `Dashboard.md`
2. Monitor `/Inbox` for new items
3. Process items in `/Needs_Action`
4. Archive completed items to `/Done`
5. Review logs for errors or issues

### Weekly Maintenance
1. Check for system updates
2. Review log files for unusual activity
3. Verify backup integrity
4. Test external service connections
5. Update documentation as needed

### Monthly Maintenance
1. Rotate credentials
2. Review access logs
3. Update security configurations
4. Check system performance
5. Review and update Company Handbook if needed

## Troubleshooting Shortcuts

### Quick Checks
- Is Claude Code running? `claude --version`
- Are MCP servers accessible? `claude mcp status`
- Is vault accessible? `ls -la AI_Employee_Vault/`
- Are credentials valid? Check `.env` file

### Common Fixes
- Restart MCP servers: `claude mcp restart`
- Refresh Claude Code: Restart Claude Code application
- Check network: `ping google.com`
- Check permissions: `ls -la filename`

## Directory Structure
```
personal-ai-employee/
├── .env                    # Environment variables
├── .mcp/                   # MCP server configuration
│   └── config.json
├── AI_Employee_Vault/      # Obsidian vault
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Inbox/
│   ├── Needs_Action/
│   └── Done/
├── setup-scripts/          # Setup scripts
├── specs/                  # Specifications
└── docs/                   # Documentation
```

## Emergency Procedures

### Immediate Actions
1. Stop all automated processes
2. Secure credentials and sensitive data
3. Notify human supervisor
4. Document the issue
5. Begin recovery procedures

### Service Unavailable
1. Switch to manual monitoring
2. Alert stakeholders
3. Check service status pages
4. Implement backup procedures
5. Resume operations when stable

## Contact Information

### Support Resources
- Claude Code documentation
- Obsidian community forums
- Project GitHub repository
- Personal AI Employee community

### Internal Contacts
- Primary supervisor: [Your name/contact]
- Backup supervisor: [Backup contact]
- IT support: [Contact information]

## Quick Checks Before Going Live

### Pre-deployment Checklist
- [ ] All MCP servers configured and running
- [ ] Claude Code can access all required services
- [ ] Obsidian vault structure correct
- [ ] Credentials stored securely
- [ ] Security measures implemented
- [ ] Backup procedures tested
- [ ] Human-in-the-loop procedures established
- [ ] Audit logging configured

## Performance Indicators

### Key Metrics
- System uptime: Target >99%
- Response time: Under 30 seconds
- Error rate: Under 1%
- Task completion rate: >95%

### Monitoring
- Daily: System health checks
- Weekly: Performance review
- Monthly: Comprehensive audit
- Quarterly: Security review

## Common Variable Names
- `CLAUDE_API_KEY`: Claude Code API key
- `EMAIL_USERNAME`: Email username
- `EMAIL_PASSWORD`: Email password/app password
- `EMAIL_IMAP_SERVER`: IMAP server address
- `EMAIL_SMTP_SERVER`: SMTP server address
- `MCP_SERVER_PORT`: MCP server port
- `VAULT_PATH`: Path to Obsidian vault