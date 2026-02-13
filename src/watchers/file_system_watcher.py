#!/usr/bin/env python3
"""
File System Watcher for AI Employee Vault

Monitors designated folders for new files and creates markdown files in
the Needs_Action directory with appropriate metadata.
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import argparse


class FileWatcherHandler(FileSystemEventHandler):
    def __init__(self, monitored_dir, vault_needs_action_dir):
        self.monitored_dir = Path(monitored_dir)
        self.vault_needs_action_dir = Path(vault_needs_action_dir)

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        print(f"New file detected: {file_path}")

        # Create markdown file in Needs_Action directory
        self.create_markdown_entry(file_path)

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Avoid processing files we just created
        needs_action_files = [f for f in self.vault_needs_action_dir.glob("FILE_*.md")]
        for md_file in needs_action_files:
            if str(file_path) in md_file.read_text():
                return  # Skip if this is a file we just processed

        print(f"Modified file detected: {file_path}")
        self.create_markdown_entry(file_path)

    def create_markdown_entry(self, file_path):
        """Create a markdown entry in the Needs_Action directory."""
        try:
            file_path = Path(file_path)

            # Generate unique ID based on timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = f"{timestamp}_{file_path.stem}"

            # Create markdown filename
            md_filename = f"FILE_{unique_id}.md"
            md_filepath = self.vault_needs_action_dir / md_filename

            # Get file metadata
            stat = file_path.stat()

            # Create markdown content
            content = f"""---
title: "File Processing Request: {file_path.name}"
created: {datetime.now().isoformat()}
file_path: "{file_path}"
file_size: {stat.st_size}
file_type: "{file_path.suffix}"
status: pending
priority: medium
---

# File Processing Request

## File Information
- **Original Path**: `{file_path}`
- **File Name**: `{file_path.name}`
- **File Size**: {stat.st_size} bytes
- **File Type**: {file_path.suffix}
- **Created**: {datetime.fromtimestamp(stat.st_ctime)}
- **Modified**: {datetime.fromtimestamp(stat.st_mtime)}

## Action Required
Process the file located at `{file_path}` according to company handbook guidelines.

## File Content Preview
```
{self.get_file_preview(file_path)}
```

## Instructions
1. Review the file content above
2. Determine appropriate action based on Company Handbook rules
3. Execute the required action
4. Move this file to Done when completed
5. Update Dashboard with status

## Status
- [ ] File reviewed
- [ ] Action determined
- [ ] Action executed
- [ ] Status updated
"""

            # Write markdown file
            with open(md_filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"Created markdown entry: {md_filepath}")

        except Exception as e:
            print(f"Error creating markdown entry for {file_path}: {str(e)}")

    def get_file_preview(self, file_path, max_lines=10):
        """Get a preview of the file content."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        if i == max_lines:  # Only add this once
                            lines.append("... (truncated)")
                        break
                    lines.append(line.rstrip())
                return "\n".join(lines)
        except Exception:
            return "[Unable to read file content - binary or inaccessible file]"


def main():
    parser = argparse.ArgumentParser(description='File System Watcher for AI Employee Vault')
    parser.add_argument('--monitored-dir', default='./watch_input',
                       help='Directory to monitor for new files (default: ./watch_input)')
    parser.add_argument('--vault-dir', default='./AI_Employee_Vault',
                       help='Vault directory containing Needs_Action folder (default: ./AI_Employee_Vault)')

    args = parser.parse_args()

    # Validate directories
    monitored_dir = Path(args.monitored_dir)
    vault_dir = Path(args.vault_dir)
    needs_action_dir = vault_dir / 'Needs_Action'

    if not monitored_dir.exists():
        print(f"Creating monitored directory: {monitored_dir}")
        monitored_dir.mkdir(parents=True, exist_ok=True)

    if not needs_action_dir.exists():
        print(f"Vault Needs_Action directory does not exist: {needs_action_dir}")
        return 1

    # Create the event handler
    event_handler = FileWatcherHandler(monitored_dir, needs_action_dir)

    # Create observer
    observer = Observer()
    observer.schedule(event_handler, str(monitored_dir), recursive=True)

    print(f"Starting file system watcher...")
    print(f"Monitoring: {monitored_dir}")
    print(f"Output to: {needs_action_dir}")
    print("Press Ctrl+C to stop.")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file system watcher...")
        observer.stop()

    observer.join()
    print("File system watcher stopped.")


if __name__ == "__main__":
    main()