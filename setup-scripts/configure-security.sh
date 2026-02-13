#!/bin/bash

# Security Configuration Script for Personal AI Employee Hackathon 0 Foundation

echo "Setting up secure credential storage mechanisms..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    touch .env
    echo "# Personal AI Employee Credentials" > .env
    echo "# Add your credentials here (these will not be committed)" >> .env
    echo "# GMAIL_USERNAME=" >> .env
    echo "# GMAIL_PASSWORD=" >> .env
    echo "# WHATSAPP_SESSION=" >> .env
    echo "# BANKING_API_KEY=" >> .env
fi

# Verify .env is in .gitignore
if grep -q ".env" .gitignore; then
    echo "✓ .env is already in .gitignore"
else
    echo ".env" >> .gitignore
    echo "✓ Added .env to .gitignore"
fi

# Create security documentation
if [ ! -d "docs" ]; then
    mkdir docs
fi

cat > docs/security-best-practices.md << 'EOF'
# Security Best Practices for Personal AI Employee

## Credential Management
- Store all sensitive credentials in the .env file
- Never commit .env files to version control
- Use environment-specific configuration files
- Rotate credentials regularly

## Access Control
- Limit access to sensitive data
- Use encrypted storage for credentials
- Implement proper authentication for external services
- Monitor access logs regularly

## Data Protection
- Encrypt sensitive data at rest
- Use secure communication protocols (HTTPS/TLS)
- Sanitize all inputs from external sources
- Implement proper error handling without exposing sensitive information

## Regular Maintenance
- Update dependencies regularly
- Review and rotate credentials monthly
- Audit access permissions periodically
- Monitor for security vulnerabilities
EOF

echo "✓ Security documentation created"

# Create credential rotation procedure
cat > docs/credential-rotation.md << 'EOF'
# Credential Rotation Procedure

## Monthly Rotation Schedule
- Gmail API credentials: First Monday of each month
- WhatsApp Web session: Mid-month check
- Banking API keys: Beginning of month
- Other service credentials: As needed based on service requirements

## Rotation Steps
1. Generate new credentials from service provider
2. Update .env file with new credentials
3. Restart services to pick up new credentials
4. Test connectivity with new credentials
5. Disable old credentials at service provider
6. Update documentation if needed

## Monitoring
- Set calendar reminders for rotation dates
- Monitor service logs for authentication failures
- Track credential expiration dates
- Maintain backup credentials for emergencies
EOF

echo "✓ Credential rotation documentation created"

echo "Security configuration completed!"