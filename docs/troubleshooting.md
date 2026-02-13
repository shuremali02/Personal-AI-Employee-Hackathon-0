# Troubleshooting Guide for Personal AI Employee Foundation Setup

## Overview
This guide provides solutions for common issues encountered during the setup and operation of the Personal AI Employee Foundation. Follow these steps in order to resolve problems.

## Installation Issues

### Python 3.13+ Installation
**Problem**: Cannot install or locate Python 3.13+
**Solution**:
1. Check current Python version: `python3 --version`
2. On Ubuntu/Debian: `sudo apt update && sudo apt install python3.13`
3. On macOS: `brew install python@3.13`
4. On Windows: Download from python.org and ensure it's in PATH
5. Verify installation: `python3.13 --version` or create alias

**Alternative Solution**:
- Use pyenv to manage Python versions: `pyenv install 3.13.0`

### Node.js v24+ LTS Installation
**Problem**: Cannot install or locate Node.js v24+ LTS
**Solution**:
1. Check current version: `node --version`
2. Use NodeSource repository for latest LTS:
   - Ubuntu: `curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash - && sudo apt-get install -y nodejs`
   - macOS: `brew install node@24`
   - Windows: Download from nodejs.org

**Alternative Solution**:
- Use nvm (Node Version Manager): `nvm install 24 && nvm use 24`

### Claude Code Not Found
**Problem**: Command 'claude' not found
**Solution**:
1. Verify Claude Code is installed and accessible
2. Check if Claude Code is in your PATH: `which claude`
3. If using Claude Code Router, ensure it's properly configured
4. Restart terminal or reload shell configuration: `source ~/.bashrc`

### uv Package Manager Issues
**Problem**: uv not found or not working properly
**Solution**:
1. Install uv: `pip install uv`
2. Or install via other methods: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Verify installation: `uv --version`
4. Add to PATH if necessary

## Configuration Issues

### Obsidian Vault Not Accessible
**Problem**: Claude Code cannot access Obsidian vault
**Solution**:
1. Verify vault directory exists: `ls -la AI_Employee_Vault/`
2. Check permissions: `ls -la AI_Employee_Vault/ | head -10`
3. Ensure Claude Code has filesystem access permissions
4. Verify vault path is correctly configured in Claude Code

### MCP Server Connection Failures
**Problem**: Claude Code cannot connect to MCP servers
**Solution**:
1. Check if MCP servers are running: `ps aux | grep mcp`
2. Verify MCP configuration in `.mcp/config.json`
3. Check if required ports are available: `netstat -tuln | grep 808[1-3]`
4. Ensure firewall allows local connections
5. Restart MCP servers: `claude mcp restart`

### Credential Exposure Warnings
**Problem**: Credentials appearing in logs or version control
**Solution**:
1. Verify `.env` is in `.gitignore`: `cat .gitignore | grep .env`
2. Remove any accidentally committed credential files
3. Regenerate exposed credentials immediately
4. Check logs for credential exposure: `grep -r "KEY\|SECRET\|TOKEN" logs/`

## Security Issues

### Git Committing Sensitive Files
**Problem**: Accidentally committing sensitive files to git
**Solution**:
1. Remove sensitive files from git history: `git filter-repo --path .env --invert-paths`
2. Ensure `.gitignore` properly excludes sensitive files
3. Regenerate any exposed credentials
4. Verify no sensitive data remains in git history

### Permission Denied Errors
**Problem**: Permission denied when accessing files or directories
**Solution**:
1. Check file permissions: `ls -la <filename>`
2. Fix permissions: `chmod 600 .env` for sensitive files
3. Fix directory permissions: `chmod 755 directory/`
4. Verify ownership: `chown -R $USER:$USER project-directory/`

### Firewall Blocking Local Connections
**Problem**: MCP servers cannot communicate due to firewall
**Solution**:
1. Check firewall status: `sudo ufw status` (Ubuntu) or `sudo firewall-cmd --list-all` (CentOS/RHEL)
2. Allow local connections: `sudo ufw allow from 127.0.0.1` (Ubuntu)
3. For Windows, check Windows Defender Firewall settings
4. Restart services after firewall changes

## Runtime Issues

### Claude Code MCP Server Startup Failures
**Problem**: MCP servers fail to start
**Solution**:
1. Check Claude Code MCP status: `claude mcp status`
2. Review MCP logs: Check Claude Code's MCP log directory
3. Verify configuration files are valid JSON
4. Check for port conflicts
5. Restart Claude Code application

### External Service Connection Failures
**Problem**: Cannot connect to external services (email, APIs, etc.)
**Solution**:
1. Verify credentials in `.env` file
2. Check network connectivity: `ping google.com`
3. Verify service-specific settings (IMAP/SMTP servers, API endpoints)
4. Check rate limits and wait if exceeded
5. Test connection with external tools first

### Obsidian Plugin Issues
**Problem**: Obsidian plugins not working with AI Employee
**Solution**:
1. Verify required plugins are installed and enabled
2. Check plugin compatibility with current Obsidian version
3. Verify vault is not in sync mode if local access is required
4. Check plugin permissions and settings

## Performance Issues

### Slow Response Times
**Problem**: AI Employee responding slowly
**Solution**:
1. Check system resources: `htop` or `top`
2. Verify adequate RAM (8GB+ recommended)
3. Check disk space: `df -h`
4. Optimize vault size by archiving old notes
5. Review and optimize Claude Code settings

### High Memory Usage
**Problem**: Excessive memory consumption
**Solution**:
1. Monitor memory usage: `free -h`
2. Close unnecessary applications
3. Review vault size and complexity
4. Consider increasing swap space if needed
5. Check for memory leaks in custom scripts

## Verification Issues

### Setup Verification Fails
**Problem**: Verification script indicates failures
**Solution**:
1. Run verification script with verbose output: `python specs/001-foundation-setup/verify_setup.py`
2. Address each failed check individually
3. Verify all required directories exist
4. Check all required files are present
5. Confirm all services are accessible

### Task Completion Indicators Incorrect
**Problem**: Tasks appear incomplete when they should be complete
**Solution**:
1. Manually verify the task requirements
2. Check file existence and correctness
3. Update task status manually if confirmed complete
4. Rerun verification steps if needed

## Network Issues

### VPN Interference
**Problem**: VPN blocking local service communication
**Solution**:
1. Temporarily disable VPN to test
2. Configure VPN split tunneling for localhost
3. Add local addresses to VPN bypass list
4. Use alternative network configuration

### Proxy Configuration Problems
**Problem**: Corporate proxy blocking connections
**Solution**:
1. Configure npm/yarn to use proxy: `npm config set proxy http://proxy.company.com:port`
2. Configure git for proxy: `git config --global http.proxy http://proxy.company.com:port`
3. Set environment variables: `HTTP_PROXY`, `HTTPS_PROXY`
4. Verify proxy allows local connections

## Recovery Procedures

### Complete Reset
**Problem**: Need to reset entire setup
**Solution**:
1. Backup important data: `cp -r AI_Employee_Vault/ vault_backup/`
2. Remove setup: `rm -rf .mcp/ setup-scripts/`
3. Clean up configurations and reinstall
4. Restore data from backup after fresh setup

### Partial Recovery
**Problem**: Specific components failing
**Solution**:
1. Identify the failing component
2. Check its configuration files
3. Verify its dependencies are working
4. Reinstall or reconfigure only the failing component
5. Test the component independently before integrating

## When to Seek Help

### Escalation Criteria
Contact support or community when:
- Following all troubleshooting steps doesn't resolve the issue
- Security concerns arise (potential credential exposure)
- Multiple components fail simultaneously
- Performance issues persist after optimization
- Unknown error messages appear

### Resources
- Claude Code documentation and support
- Obsidian community forums
- Project GitHub issues
- Personal AI Employee community channels
- System administrator assistance

## Prevention Tips

### Regular Maintenance
- Update system and dependencies regularly
- Monitor system resources and performance
- Review and update security configurations
- Test backup and recovery procedures
- Keep documentation current

### Best Practices
- Regular backups of vault and configurations
- Periodic security audits
- Monitor logs for unusual activity
- Keep sensitive information secure
- Test new configurations in isolated environments first