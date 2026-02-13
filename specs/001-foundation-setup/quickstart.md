# Quickstart Guide: Personal AI Employee Hackathon 0 - Foundation Setup

## Overview
This guide provides a streamlined approach to setting up the foundation for the Personal AI Employee Hackathon 0. Follow these steps to prepare your development environment before beginning the Bronze tier implementation.

## Prerequisites
- Administrative access to install software on your machine
- Stable internet connection for downloading components
- Hardware meeting minimum requirements (8GB RAM, 4-core CPU)

## Step 1: Install Required Software
1. Install Claude Code (Pro subscription or setup Claude Code Router with Free Gemini API)
2. Install Obsidian v1.10.6+
3. Install Python 3.13+
4. Install Node.js v24+ LTS
5. Install GitHub Desktop

Verify installations:
```bash
claude --version
python --version
node --version
git --version
```

## Step 2: Create Obsidian Vault
1. Create a new Obsidian vault named "AI_Employee_Vault"
2. Set up the folder structure:
   ```
   AI_Employee_Vault/
   ├── Dashboard.md
   ├── Company_Handbook.md
   ├── Inbox/
   ├── Needs_Action/
   └── Done/
   ```

## Step 3: Configure Security
1. Create a `.env` file in your project root
2. Add to `.gitignore` to prevent committing credentials
3. Set up secure credential storage (Keychain, Credential Manager, or 1Password CLI)
4. Document credential rotation procedures

## Step 4: Set Up MCP Servers
1. Install the basic MCP server framework
2. Configure filesystem MCP (built-in with Claude Code)
3. Test MCP server connectivity with Claude Code
4. Prepare configuration for additional MCP servers

## Step 5: Configure External Services
1. Set up Gmail API access (if using Gmail watcher)
2. Configure WhatsApp Web session (if using WhatsApp watcher)
3. Set up any banking API access (if using finance watcher)
4. Test external API connectivity

## Step 6: Initialize Project Structure
1. Clone or initialize the project repository
2. Set up proper directory structure for specs, plans, and tasks
3. Configure git with proper remotes and branches
4. Set up `.gitignore` with appropriate exclusions

## Step 7: Verification
1. Verify Claude Code can read/write to Obsidian vault
2. Test security measures prevent unauthorized access
3. Confirm external APIs are accessible and responsive
4. Verify MCP servers are discoverable and responsive
5. Test development environment supports efficient work

## Next Steps
Once all foundation setup is complete:
1. Verify all setup checklist items are complete
2. Test basic functionality of each component
3. Document any issues or deviations from plan
4. Begin Bronze tier implementation following the established foundation
5. Ensure all security measures are properly implemented before proceeding

## Troubleshooting
- If Claude Code doesn't work: Check subscription status and API access
- If Obsidian vault doesn't sync properly: Ensure local-first approach is maintained
- If MCP servers don't connect: Verify network connectivity and firewall settings
- If external APIs fail: Check credentials and rate limits