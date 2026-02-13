#!/usr/bin/env python3
"""
IMAP Email Watcher for AI Employee Vault

Monitors email account via IMAP for new messages and creates markdown files in
the Needs_Action directory with appropriate metadata.
"""

import os
import time
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from imap_tools import MailBox, AND
import html2text


class EmailIMAPWatcher:
    """Class to handle email monitoring via IMAP."""

    def __init__(self, vault_needs_action_dir):
        # Load environment variables
        load_dotenv()

        self.vault_needs_action_dir = Path(vault_needs_action_dir)
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.gmail_api_key = os.getenv('GMAIL_API_KEY')

        # For Gmail, the server is always imap.gmail.com
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993

        if not self.email_address or not self.email_password:
            raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set in environment variables")

        self.mailbox = None
        self.last_check_time = None

    def connect(self):
        """Connect to the email account via IMAP."""
        try:
            self.mailbox = MailBox(self.imap_server, port=self.imap_port).login(
                self.email_address,
                self.email_password
            )
            print(f"✅ Successfully connected to email account: {self.email_address}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to email account: {str(e)}")
            return False

    def get_recent_emails(self, max_results=10):
        """Get recent unread emails from the mailbox."""
        try:
            # Set the search criteria
            if self.last_check_time:
                # Only get emails received after the last check
                search_criteria = AND(seen=False, date_gte=self.last_check_time.date())
            else:
                # Get all unread emails
                search_criteria = AND(seen=False)

            # Fetch emails
            emails = []
            for msg in self.mailbox.fetch(search_criteria, limit=max_results):
                email_info = {
                    'uid': msg.uid,
                    'subject': msg.subject or "No Subject",
                    'from': msg.from_,
                    'to': msg.to,
                    'date': msg.date_str,
                    'body_text': msg.text or self.html_to_text(msg.html) or "No body content",
                    'body_html': msg.html or "",
                    'flags': msg.flags,
                    'size': msg.size_rfc822,
                    'headers': dict(msg.headers)
                }
                emails.append(email_info)

            # Update last check time
            self.last_check_time = datetime.now()

            return emails

        except Exception as e:
            print(f"❌ Error fetching emails: {str(e)}")
            return []

    def html_to_text(self, html_content):
        """Convert HTML email content to plain text."""
        if not html_content:
            return ""

        try:
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            h.body_width = 0  # Don't wrap lines
            return h.handle(html_content)
        except Exception:
            # If html2text fails, do basic stripping
            import re
            clean = re.sub('<[^<]+?>', '', html_content)
            return clean

    def create_markdown_entry(self, email_info):
        """Create a markdown entry in the Needs_Action directory."""
        try:
            # Generate unique ID based on timestamp and email UID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = f"{timestamp}_{str(email_info['uid'])[:8]}"

            # Create markdown filename
            safe_subject = "".join(c for c in email_info['subject'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            if not safe_subject:
                safe_subject = "untitled_email"
            md_filename = f"EMAIL_{unique_id}_{safe_subject[:50]}.md"
            md_filepath = self.vault_needs_action_dir / md_filename

            # Determine if email needs approval based on content
            content_lower = email_info['body_text'].lower()
            if any(keyword in content_lower for keyword in ['budget', '$', 'funds', 'approval', 'authorize', 'spend']):
                action_required = "send_to_approval"
            elif any(keyword in content_lower for keyword in ['urgent', 'asap', 'immediately', 'critical']):
                action_required = "urgent_processing"
            elif any(keyword in content_lower for keyword in ['plan', 'schedule', 'organize', 'arrange']):
                action_required = "create_plan"
            else:
                action_required = "standard_processing"

            # Create markdown content
            content = f"""---
title: "Email Processing Request: {email_info['subject']}"
created: {datetime.now().isoformat()}
email_uid: "{email_info['uid']}"
email_from: "{email_info['from']}"
email_to: "{str(email_info['to'])}"
email_date: "{email_info['date']}"
status: pending
priority: medium
action_required: {action_required}
---

# Email Processing Request

## Email Information
- **Subject**: {email_info['subject']}
- **From**: `{email_info['from']}`
- **To**: `{str(email_info['to'])}`
- **Date**: {email_info['date']}
- **Size**: {email_info['size']} bytes
- **UID**: `{email_info['uid']}`

## Email Content
{email_info['body_text'][:2000]}{'...' if len(email_info['body_text']) > 2000 else ''}

## Action Required
Review this email and determine appropriate action based on Company Handbook guidelines.

## Instructions
1. Review the email content above
2. Determine appropriate action based on Company Handbook rules
3. Execute the required action
4. Move this file to Done when completed
5. Update Dashboard with status

## Status
- [ ] Email reviewed
- [ ] Action determined
- [ ] Action executed
- [ ] Status updated
"""

            # Write markdown file
            with open(md_filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Created email entry: {md_filepath.name}")

            # Mark email as read after processing
            try:
                self.mailbox.flag([email_info['uid']], ['\\Seen'], True)
            except Exception as e:
                print(f"⚠️ Could not mark email as read: {e}")

        except Exception as e:
            print(f"❌ Error creating markdown entry for email: {str(e)}")

    def process_new_emails(self):
        """Process any new unread emails."""
        try:
            emails = self.get_recent_emails()
            processed_count = 0

            for email in emails:
                self.create_markdown_entry(email)
                processed_count += 1

            return processed_count

        except Exception as e:
            print(f"❌ Error processing emails: {str(e)}")
            return 0

    def run_monitoring(self, check_interval=300):  # Default: check every 5 minutes
        """Run continuous monitoring for new emails."""
        print(f"Starting email monitoring...")
        print(f"Checking for new emails every {check_interval} seconds")

        try:
            while True:
                print(f"📧 Checking for new emails at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

                count = self.process_new_emails()
                if count > 0:
                    print(f"✅ Processed {count} new emails")
                else:
                    print("📭 No new emails found")

                print(f"⏳ Sleeping for {check_interval} seconds...")
                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n🛑 Stopping email watcher...")
        except Exception as e:
            print(f"❌ Error in monitoring loop: {str(e)}")


def main():
    import argparse

    # Load environment first
    load_dotenv()

    parser = argparse.ArgumentParser(description='IMAP Email Watcher for AI Employee Vault')
    parser.add_argument('--vault-dir', default='./AI_Employee_Vault',
                       help='Vault directory containing Needs_Action folder (default: ./AI_Employee_Vault)')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300 for 5 minutes)')

    args = parser.parse_args()

    # Validate vault directory
    vault_dir = Path(args.vault_dir)
    needs_action_dir = vault_dir / 'Needs_Action'

    if not needs_action_dir.exists():
        print(f"❌ Vault Needs_Action directory does not exist: {needs_action_dir}")
        return 1

    # Check if email credentials are available
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    if not email_address or not email_password:
        print("❌ EMAIL_ADDRESS and EMAIL_PASSWORD must be set in environment variables!")
        print("📝 Please set them in your .env file or environment:")
        print("   EMAIL_ADDRESS=your_email@gmail.com")
        print("   EMAIL_PASSWORD=your_app_password")
        return 1

    # Create the email watcher
    email_watcher = EmailIMAPWatcher(needs_action_dir)

    try:
        # Connect to email account
        if not email_watcher.connect():
            return 1

        print("🤖 Email watcher initialized successfully!")
        print(f"📧 Monitoring email account: {email_address}")
        print(f"📋 Email entries will be created in: {needs_action_dir}")
        print("⚠️ Press Ctrl+C to stop.")
        print()

        # Run the monitoring
        email_watcher.run_monitoring(args.interval)

    except Exception as e:
        print(f"❌ Error initializing email watcher: {str(e)}")
        return 1

    return 0


if __name__ == "__main__":
    main()