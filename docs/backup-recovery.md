# Backup and Recovery Procedures for Personal AI Employee

## Overview
This document provides comprehensive procedures for backing up and recovering the Personal AI Employee foundation setup. These procedures ensure continuity of operations and protect against data loss or system failures.

## Backup Strategy

### 1. Backup Categories
- **Critical**: Essential for system operation (configuration files, credentials)
- **Important**: Important for functionality (vault content, custom scripts)
- **Archive**: Historical data (completed tasks, old logs)

### 2. Backup Schedule
- **Daily**: Vault content, logs, temporary files
- **Weekly**: Configuration files, custom scripts, system settings
- **Monthly**: Complete system backup, historical data
- **On-demand**: Before major updates, configuration changes

### 3. Backup Locations
- **Local**: External drive or separate partition (recommended)
- **Network**: Network Attached Storage (NAS) for redundancy
- **Cloud**: Encrypted cloud storage for off-site backup (optional)

## Critical Backup Items

### 1. Configuration Files
- `.env` - Contains sensitive credentials (encrypt before backup)
- `.mcp/config.json` - MCP server configuration
- `AI_Employee_Vault/Company_Handbook.md` - Rules of engagement
- `AI_Employee_Vault/Dashboard.md` - System status information

### 2. Vault Content
- All files in `AI_Employee_Vault/` excluding temporary files
- Important: Encrypt sensitive information before backup
- Maintain folder structure: `/Inbox`, `/Needs_Action`, `/Done`

### 3. Custom Scripts
- All Python scripts in `src/` directory
- MCP server implementations
- Watcher scripts
- Setup and utility scripts

## Backup Procedures

### 1. Automated Daily Backup
```bash
#!/bin/bash
# daily-backup.sh - Daily backup script

BACKUP_DIR="/path/to/backup/personal-ai-employee-$(date +%Y%m%d)"
VAULT_SOURCE="./AI_Employee_Vault"
CONFIG_FILES=".env .mcp/config.json AI_Employee_Vault/Company_Handbook.md AI_Employee_Vault/Dashboard.md"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup configuration files (excluding .env for security)
mkdir -p "$BACKUP_DIR/config"
for file in $CONFIG_FILES; do
    if [ "$file" != ".env" ]; then
        cp "$file" "$BACKUP_DIR/config/" 2>/dev/null || echo "Warning: Could not backup $file"
    fi
done

# Backup vault content (excluding sensitive logs)
mkdir -p "$BACKUP_DIR/vault"
rsync -av --exclude="*.log" --exclude="*.tmp" "$VAULT_SOURCE/" "$BACKUP_DIR/vault/"

# Create encrypted backup of .env file
if [ -f ".env" ]; then
    openssl enc -aes-256-cbc -salt -in .env -out "$BACKUP_DIR/config/.env.enc" -k "$ENCRYPTION_KEY"
fi

# Compress backup
tar -czf "$BACKUP_DIR.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"

# Cleanup temporary directory
rm -rf "$BACKUP_DIR"

echo "Daily backup completed: $BACKUP_DIR.tar.gz"
```

### 2. Weekly Full Backup
```bash
#!/bin/bash
# weekly-full-backup.sh - Weekly full system backup

BACKUP_DIR="/path/to/backup/personal-ai-employee-full-$(date +%Y%m%d)"
SOURCE_ROOT="."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup entire project except unnecessary files
rsync -av \
    --exclude=".git/" \
    --exclude="node_modules/" \
    --exclude="__pycache__/" \
    --exclude="*.pyc" \
    --exclude="*.log" \
    --exclude="*.tmp" \
    --exclude=".pytest_cache/" \
    --exclude=".coverage" \
    "$SOURCE_ROOT/" "$BACKUP_DIR/project/"

# Backup encrypted .env file separately
if [ -f ".env" ]; then
    openssl enc -aes-256-cbc -salt -in .env -out "$BACKUP_DIR/encrypted-env.enc" -k "$ENCRYPTION_KEY"
fi

# Create backup manifest
find "$BACKUP_DIR" -type f | sort > "$BACKUP_DIR/MANIFEST.txt"

# Compress and encrypt the entire backup
tar -czf "$BACKUP_DIR.tar.gz" -C "$(dirname "$BACKUP_DIR")" "$(basename "$BACKUP_DIR")"

echo "Weekly full backup completed: $BACKUP_DIR.tar.gz"
```

### 3. Manual Backup Command
```bash
# Quick manual backup
BACKUP_NAME="personal-ai-employee-backup-$(date +%Y%m%d-%H%M%S)"
tar --exclude='.git' --exclude='node_modules' --exclude='*.log' -czf "$BACKUP_NAME.tar.gz" ./
```

## Recovery Procedures

### 1. System Recovery Overview
Recovery should follow this order:
1. System restoration (OS, applications)
2. Configuration files restoration
3. MCP server setup
4. Vault content restoration
5. Service verification

### 2. Complete System Recovery
```bash
#!/bin/bash
# complete-recovery.sh - Complete system recovery script

RESTORE_BACKUP="$1"  # Path to backup file
TARGET_DIR="${2:-.}" # Target directory (default: current)

if [ ! -f "$RESTORE_BACKUP" ]; then
    echo "Error: Backup file not found: $RESTORE_BACKUP"
    exit 1
fi

# Extract backup
TEMP_DIR=$(mktemp -d)
tar -xzf "$RESTORE_BACKUP" -C "$TEMP_DIR"

# Stop all services
echo "Stopping MCP servers..."
claude mcp stop 2>/dev/null || echo "Claude MCP not running or not available"

# Restore configuration files (except .env)
if [ -d "$TEMP_DIR/*/config" ]; then
    CONFIG_DIR=$(find "$TEMP_DIR" -name "config" -type d | head -1)
    cp -r "$CONFIG_DIR"/* "$TARGET_DIR/" 2>/dev/null
fi

# Restore vault content
if [ -d "$TEMP_DIR/*/vault" ]; then
    VAULT_DIR=$(find "$TEMP_DIR" -name "vault" -type d | head -1)
    rsync -av "$VAULT_DIR/" "$TARGET_DIR/AI_Employee_Vault/"
fi

# Restore project files (if full backup)
if [ -d "$TEMP_DIR/*/project" ]; then
    PROJECT_DIR=$(find "$TEMP_DIR" -name "project" -type d | head -1)
    rsync -av "$PROJECT_DIR/" "$TARGET_DIR/"
fi

# Restore encrypted .env file if present
if [ -f "$TEMP_DIR/*/config/.env.enc" ]; then
    ENCRYPTED_ENV=$(find "$TEMP_DIR" -name ".env.enc" -type f | head -1)
    openssl enc -aes-256-cbc -d -in "$ENCRYPTED_ENV" -out "$TARGET_DIR/.env" -k "$ENCRYPTION_KEY"
elif [ -f "$TEMP_DIR/*/encrypted-env.enc" ]; then
    openssl enc -aes-256-cbc -d -in "$TEMP_DIR/*/encrypted-env.enc" -out "$TARGET_DIR/.env" -k "$ENCRYPTION_KEY"
fi

# Clean up
rm -rf "$TEMP_DIR"

echo "Restore completed. Please verify configuration and restart services."
```

### 3. Partial Recovery (Vault Only)
```bash
# Restore only vault content
BACKUP_FILE="backup-file.tar.gz"
TEMP_DIR=$(mktemp -d)
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
rsync -av "$TEMP_DIR/*/vault/" "./AI_Employee_Vault/"
rm -rf "$TEMP_DIR"
```

## Verification Procedures

### 1. Post-Recovery Verification
After any recovery operation, verify:

1. **System Status**:
   ```bash
   claude --version
   python3 --version
   node --version
   ```

2. **Configuration Files**:
   ```bash
   ls -la .env .mcp/config.json AI_Employee_Vault/
   ```

3. **MCP Servers**:
   ```bash
   claude mcp status
   ```

4. **Vault Access**:
   ```bash
   ls -la AI_Employee_Vault/
   cat AI_Employee_Vault/Dashboard.md
   ```

### 2. Automated Verification Script
```bash
#!/bin/bash
# verify-recovery.sh - Post-recovery verification

echo "=== Personal AI Employee Recovery Verification ==="

# Check essential commands
echo "Checking essential commands..."
COMMANDS=("claude" "python3" "node" "uv")
for cmd in "${COMMANDS[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        echo "✅ $cmd: $(eval "$cmd --version" 2>&1)"
    else
        echo "❌ $cmd: NOT FOUND"
    fi
done

# Check configuration files
echo -e "\nChecking configuration files..."
CONFIG_FILES=(".env" ".mcp/config.json" "AI_Employee_Vault/Dashboard.md" "AI_Employee_Vault/Company_Handbook.md")
for file in "${CONFIG_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file: EXISTS ($(stat -c%s "$file") bytes)"
    else
        echo "❌ $file: MISSING"
    fi
done

# Check vault structure
echo -e "\nChecking vault structure..."
VAULT_FOLDERS=("AI_Employee_Vault/Inbox" "AI_Employee_Vault/Needs_Action" "AI_Employee_Vault/Done")
for folder in "${VAULT_FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        COUNT=$(find "$folder" -type f | wc -l)
        echo "✅ $folder: EXISTS ($COUNT files)"
    else
        echo "❌ $folder: MISSING"
    fi
done

# Check MCP status
echo -e "\nChecking MCP status..."
if claude mcp status &> /dev/null; then
    echo "✅ MCP: RUNNING"
else
    echo "⚠️  MCP: NOT RUNNING (may need to start manually)"
fi

echo -e "\n=== Verification Complete ==="
```

## Disaster Recovery Scenarios

### 1. Minor Data Loss
**Scenario**: Individual file corruption or accidental deletion
**Procedure**:
1. Identify the lost/deleted file
2. Locate the most recent backup containing the file
3. Restore only the specific file
4. Verify the restored file's integrity
5. Test system functionality

### 2. Major System Failure
**Scenario**: Complete system crash or hardware failure
**Procedure**:
1. Set up new system with required software
2. Download the latest full backup
3. Execute complete system recovery
4. Verify all components are functional
5. Test all critical workflows

### 3. Security Incident
**Scenario**: Suspected credential exposure or unauthorized access
**Procedure**:
1. Immediately stop all automated processes
2. Restore from backup before the incident
3. Rotate all credentials
4. Review and update security configurations
5. Implement additional security measures
6. Verify system integrity before resuming operations

## Security Considerations

### 1. Encrypted Backups
Always encrypt sensitive data in backups:
```bash
# Create encrypted backup
tar -czf - ./sensitive-data/ | openssl enc -aes-256-cbc -e -out backup-encrypted.tar.gz.enc -k "$ENCRYPTION_KEY"

# Restore encrypted backup
openssl enc -aes-256-cbc -d -in backup-encrypted.tar.gz.enc -k "$ENCRYPTION_KEY" | tar -xzvf -
```

### 2. Access Control
- Restrict access to backup files to authorized personnel only
- Use strong encryption keys and store them separately
- Regularly rotate encryption keys
- Monitor access to backup storage locations

### 3. Backup Integrity
- Regularly verify backup integrity with checksums
- Test recovery procedures periodically
- Maintain multiple backup copies in different locations
- Document and verify the restoration process

## Maintenance Procedures

### 1. Backup Testing
- Monthly: Test restoration of critical files
- Quarterly: Perform full system recovery test
- Annually: Review and update backup procedures

### 2. Backup Storage Management
- Regular cleanup of old backups
- Monitor backup storage space
- Verify backup storage integrity
- Update backup retention policies

### 3. Procedure Updates
- Review and update procedures when system changes
- Train team members on backup procedures
- Document any procedural changes
- Maintain up-to-date contact information for recovery

## Emergency Contacts

### 1. Recovery Team
- Primary: [Your Name and Contact Information]
- Secondary: [Backup Contact Information]
- Technical Support: [Support Contact Information]

### 2. Service Providers
- Claude Code Support: [Contact Information]
- Obsidian Support: [Contact Information]
- Cloud Storage Provider: [Contact Information]

## Checklist for Backup Operations

### Daily Backup Checklist
- [ ] Run daily backup script
- [ ] Verify backup file creation
- [ ] Check backup file size (should be reasonable)
- [ ] Store backup in secure location
- [ ] Update backup log

### Recovery Checklist
- [ ] Identify scope of recovery needed
- [ ] Locate appropriate backup file
- [ ] Verify backup integrity
- [ ] Stop all services before recovery
- [ ] Execute recovery procedure
- [ ] Verify system functionality
- [ ] Update recovery log
- [ ] Notify stakeholders of completion

## Conclusion

Regular backups and tested recovery procedures are essential for maintaining the reliability and continuity of your Personal AI Employee system. Follow these procedures to ensure that your system can recover quickly and securely from any data loss or system failure event.