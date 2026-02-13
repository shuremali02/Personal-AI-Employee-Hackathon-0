# AI Employee Vault Structure Documentation

## Overview
The Obsidian vault serves as the "memory" and GUI for the AI employee, following the local-first architecture principle.

## Directory Structure

### `/Inbox`
- **Purpose**: Incoming tasks and information requiring initial processing
- **Contents**: Unprocessed emails, new tasks, incoming notifications
- **Processing**: Items are reviewed and either moved to `/Needs_Action` or `/Done`

### `/Needs_Action`
- **Purpose**: Tasks requiring action or decision from the AI employee or human supervisor
- **Contents**: Work items that need attention, pending approvals, scheduled tasks
- **Processing**: Items are worked on and eventually moved to `/Done`

### `/Done`
- **Purpose**: Completed tasks and processed information
- **Contents**: Finished work items, archived communications, completed processes
- **Processing**: Items may be periodically archived or cleaned up based on retention policy

## File Types

### Dashboard.md
- **Purpose**: Central overview of AI employee status and activities
- **Updates**: Real-time status indicators, active tasks, system health

### Company_Handbook.md
- **Purpose**: Rules of engagement and operational guidelines
- **Updates**: Policy changes, authorization levels, emergency procedures

## Access Patterns

### Read Operations
- AI employee regularly scans `/Inbox` for new items
- Monitors all folders for changes that might trigger actions

### Write Operations
- New items enter through `/Inbox`
- Processed items move to appropriate folders
- Status updates written to Dashboard.md

## Security Considerations

- All data remains local on the user's device
- No cloud sync of sensitive communications
- Credentials and sensitive information handled according to Company_Handbook.md guidelines
- Audit trail maintained for all operations