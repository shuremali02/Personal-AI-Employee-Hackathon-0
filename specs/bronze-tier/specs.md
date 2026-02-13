---
page: Bronze Tier Implementation
output: bronze-implementation/
spec: specs/bronze-tier/specs.md
word_count: 1000-1500
priority: High
---

# Bronze Tier Implementation Specification

## Purpose
This specification defines the minimum viable deliverable for the Bronze Tier of the Personal AI Employee Hackathon. The Bronze Tier serves as the foundational implementation that establishes the core architecture and basic functionality required for an autonomous AI employee system.

## Requirements Overview
Based on the hackathon document, the Bronze Tier requirements are:
- Obsidian vault with Dashboard.md and Company_Handbook.md
- One working Watcher script (Gmail OR file system monitoring)
- Claude Code successfully reading from and writing to the vault
- Basic folder structure: /Inbox, /Needs_Action, /Done
- All AI functionality should be implemented as Agent Skills

## File Structure
```
AI_Employee_Vault/
├── Dashboard.md
├── Company_Handbook.md
├── Inbox/
├── Needs_Action/
├── Done/
├── Plans/
├── Logs/
└── Pending_Approval/
```

## 1. Obsidian Vault Setup

### 1.1 Dashboard.md
**Purpose**: Real-time summary of activities and metrics
**Content structure**:
- Executive summary of current status
- Pending tasks count
- Recent activity log
- Key metrics (emails processed, actions taken)
- Quick access links to important sections

**Frontmatter**:
```yaml
---
title: "AI Employee Dashboard"
created: {{date}}
updated: {{date}}
status: active
---
```

### 1.2 Company_Handbook.md
**Purpose**: Contains rules of engagement and operational guidelines
**Content structure**:
- Communication guidelines (politeness rules, response protocols)
- Approval thresholds (when to escalate to human)
- Priority classifications
- Emergency procedures
- Contact information and escalation paths

## 2. Watcher Implementation

### 2.1 Choice of Watcher
The implementation will include ONE of the following:
- **Gmail Watcher**: Monitors Gmail for new important/unread messages
- **File System Watcher**: Monitors designated folders for new files

### 2.2 Gmail Watcher Implementation
If implementing the Gmail watcher:
- Use Google OAuth 2.0 for authentication
- Monitor for unread important emails
- Create markdown files in `/Needs_Action/` folder
- Include email metadata (sender, subject, timestamp, priority)
- Handle authentication refresh

**Dependencies**:
- google-api-python-client
- google-auth-oauthlib
- google-auth-httplib2

### 2.3 File System Watcher Implementation
If implementing the file system watcher:
- Use Python watchdog library
- Monitor designated drop folders
- Copy files to `/Needs_Action/` with metadata
- Create corresponding markdown files with file information
- Handle file system events (create, modify, delete)

**Dependencies**:
- watchdog

## 3. Claude Code Integration

### 3.1 File System Access
- Configure Claude Code to read from and write to the Obsidian vault
- Implement file system tools usage for:
  - Reading markdown files
  - Writing reports and plans
  - Moving files between folders
  - Creating new action items

### 3.2 Basic Commands
- Read and process files in `/Needs_Action/`
- Create plan files in `/Plans/`
- Move completed items to `/Done/`
- Update Dashboard.md with status
- Write to `/Pending_Approval/` for sensitive actions

## 4. Folder Structure Implementation

### 4.1 Core Directories
```
/Inbox          # Incoming items to be categorized
/Needs_Action   # Items requiring processing
/Plans          # Generated action plans
/Done           # Completed items
/Logs           # System logs and audit trail
/Pending_Approval # Items requiring human approval
```

### 4.2 File Naming Convention
- EMAIL_[unique_id].md for email notifications
- FILE_[filename].md for file drops
- PLAN_[description].md for generated plans
- APPROVAL_[action_type].md for approval requests

## 5. Agent Skills Implementation

### 5.1 Required Skills
All AI functionality must be implemented as Claude Agent Skills:

**Skill 1: FileProcessor**
- Reads files from Needs_Action
- Parses content and metadata
- Determines appropriate action

**Skill 2: Planner**
- Creates structured plan files
- Tracks progress with checkboxes
- Updates status as tasks complete

**Skill 3: FileMover**
- Moves files between vault folders
- Maintains audit trail
- Updates Dashboard with status

**Skill 4: ApprovalManager**
- Creates approval request files
- Handles human-in-the-loop workflows
- Manages approval status tracking

### 5.2 Skill Configuration
- Define skill manifests in JSON format
- Map skills to specific vault operations
- Implement proper error handling
- Include logging for audit trail

## 6. Basic Functionality Flow

### 6.1 Processing Cycle
1. Watcher detects new input (email or file)
2. Creates markdown file in `/Needs_Action/`
3. Claude Code processes the file
4. Generates plan in `/Plans/`
5. Executes actions or creates approval requests
6. Updates Dashboard.md
7. Moves items to appropriate completion folders

### 6.2 Error Handling
- Basic exception handling for file operations
- Retry mechanism for transient failures
- Logging of errors to `/Logs/`
- Graceful degradation when services unavailable

## 7. Configuration Requirements

### 7.1 Environment Setup
- Python 3.13+ with required dependencies
- Claude Code with filesystem MCP enabled
- Obsidian vault properly configured
- Credentials stored securely (not in vault)

### 7.2 MCP Configuration
```json
{
  "servers": [
    {
      "name": "filesystem",
      "type": "builtin",
      "capabilities": ["read", "write", "list"]
    }
  ]
}
```

## 8. Testing Requirements

### 8.1 Basic Tests
- Verify watcher functionality
- Test file creation in Needs_Action
- Confirm Claude Code can read/write to vault
- Validate folder structure operations
- Test approval workflow

### 8.2 Success Criteria
- At least one watcher running continuously
- Claude Code successfully processes sample files
- Files move correctly between folders
- Dashboard updates with activity
- Agent skills execute properly

## 9. Security Considerations

### 9.1 Credential Management
- Store credentials in environment variables
- Never commit sensitive data to version control
- Use secure credential storage for production

### 9.2 Access Control
- Limit file system permissions appropriately
- Validate file paths to prevent directory traversal
- Log all access for audit purposes

## 10. Deployment Instructions

### 10.1 Installation Steps
1. Install Python dependencies
2. Set up Obsidian vault
3. Configure Claude Code
4. Set up chosen watcher (Gmail or File System)
5. Configure Agent Skills
6. Test basic functionality

### 10.2 Running the System
- Start the chosen watcher script
- Initialize Claude Code in vault directory
- Monitor Dashboard for activity
- Verify logs and audit trail

## 11. Success Metrics
- System processes at least 5 test items successfully
- All required files and folders created properly
- Agent skills execute without errors
- Dashboard updates reflect system activity
- Basic workflow completes end-to-end

## 12. Deliverables
- Working Obsidian vault with required structure
- Running watcher script (Gmail or File System)
- Configured Agent Skills
- Documented installation and usage instructions
- Sample processed items demonstrating functionality

---
**Implementation Timeline**: 8-12 hours as specified in hackathon document
**Complexity**: Foundation tier requiring basic Python, file system, and Claude Code knowledge