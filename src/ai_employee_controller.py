#!/usr/bin/env python3
"""
AI Employee Controller

Main controller for the AI Employee system that integrates all components:
- File System Watcher
- Agent Skills Framework
- Vault Operations
- Dashboard Updates
"""

import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Callable

# Add the src directory to the path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from watchers.file_system_watcher import FileWatcherHandler
from skills.file_processor import FileProcessor
from skills.planner import Planner
from skills.file_mover import FileMover
from skills.approval_manager import ApprovalManager


class AIEmployeeController:
    """Main controller for the AI Employee system."""

    def __init__(self, vault_dir: str = "./AI_Employee_Vault", monitored_dir: str = "./watch_input"):
        self.vault_dir = Path(vault_dir)
        self.monitored_dir = Path(monitored_dir)

        # Initialize skills
        self.file_processor = FileProcessor(vault_dir=vault_dir)
        self.planner = Planner(vault_dir=vault_dir)
        self.file_mover = FileMover(vault_dir=vault_dir)
        self.approval_manager = ApprovalManager(vault_dir=vault_dir)

        # Ensure directories exist
        self.monitored_dir.mkdir(parents=True, exist_ok=True)

        # Initialize watcher handler
        self.watcher_handler = FileWatcherHandler(self.monitored_dir, self.vault_dir / "Needs_Action")

        # Control flag for main loop
        self.running = False

        print(f"AI Employee Controller initialized")
        print(f"- Vault directory: {self.vault_dir}")
        print(f"- Monitored directory: {self.monitored_dir}")

    def start_watcher(self):
        """Start the file system watcher in a separate thread."""
        from watchdog.observers import Observer

        self.observer = Observer()
        self.observer.schedule(self.watcher_handler, str(self.monitored_dir), recursive=True)
        self.observer.start()

        print(f"File system watcher started, monitoring: {self.monitored_dir}")

        return self.observer

    def stop_watcher(self):
        """Stop the file system watcher."""
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
            print("File system watcher stopped")

    def process_needs_action_items(self):
        """Process all items in the Needs_Action directory."""
        print("Processing items in Needs_Action directory...")

        results = self.file_processor.execute(max_files=10)

        print(f"Processed {results['summary']['files_processed']} files")
        print(f"Errors: {results['summary']['errors']}")

        for action_item in results["actions_determined"]:
            file_path = action_item["file"]
            action = action_item["action"]

            print(f"Action for {Path(file_path).name}: {action}")

            # Based on the determined action, execute appropriate skill
            self._execute_action_based_on_type(action, action_item)

    def _execute_action_based_on_type(self, action: str, action_item: Dict[str, Any]):
        """Execute appropriate action based on the determined action type."""
        file_path = action_item["file"]

        if action == "create_plan":
            self._handle_create_plan(file_path, action_item)
        elif action == "send_to_approval":
            self._handle_send_to_approval(file_path, action_item)
        elif action == "urgent_processing":
            self._handle_urgent_processing(file_path, action_item)
        elif action == "send_message":
            self._handle_send_message(file_path, action_item)
        elif action == "standard_processing":
            self._handle_standard_processing(file_path, action_item)

    def _handle_create_plan(self, file_path: str, action_item: Dict[str, Any]):
        """Handle plan creation requests."""
        print(f"Creating plan for: {Path(file_path).name}")

        # Extract plan details from the file
        parsed_data = action_item.get("parsed_data", {})
        frontmatter = parsed_data.get("frontmatter", {})

        plan_title = frontmatter.get("title", f"Plan for {Path(file_path).stem}")
        objectives = frontmatter.get("objectives", ["Process file automatically"])

        # Create tasks based on file content
        tasks = [{"description": f"Process content of {Path(file_path).name}", "priority": "medium"}]

        try:
            plan_result = self.planner.execute(
                plan_title=plan_title,
                objectives=objectives,
                tasks=tasks,
                save_to_plans=True
            )

            print(f"Plan created: {plan_result['id']}")

            # Move the original file to Plans folder (since a plan was created from it)
            self.file_mover.execute(file_path, "plans", f"Plan created: {plan_result['id']}")

        except Exception as e:
            print(f"Error creating plan: {str(e)}")

    def _handle_send_to_approval(self, file_path: str, action_item: Dict[str, Any]):
        """Handle approval requests."""
        print(f"Sending to approval: {Path(file_path).name}")

        parsed_data = action_item.get("parsed_data", {})
        frontmatter = parsed_data.get("frontmatter", {})

        action_type = frontmatter.get("action_type", "general_request")
        description = parsed_data.get("content_preview", "No description available")

        try:
            approval_result = self.approval_manager.execute(
                action_type=action_type,
                description=description,
                urgency=frontmatter.get("priority", "normal")
            )

            print(f"Approval request created: {approval_result['id']}")

            # Move the original file to Pending_Approval folder (since it's awaiting approval)
            self.file_mover.execute(file_path, "pending_approval", f"Approval created: {approval_result['id']}")

        except Exception as e:
            print(f"Error creating approval: {str(e)}")

    def _handle_urgent_processing(self, file_path: str, action_item: Dict[str, Any]):
        """Handle urgent processing requests."""
        print(f"Processing urgently: {Path(file_path).name}")

        # For urgent processing, we'll move to plans for immediate attention
        try:
            self.file_mover.execute(file_path, "plans", "Urgent processing")
        except Exception as e:
            print(f"Error in urgent processing: {str(e)}")

    def _handle_send_message(self, file_path: str, action_item: Dict[str, Any]):
        """Handle message sending requests."""
        print(f"Handling message request: {Path(file_path).name}")

        # For now, we'll move to plans for message processing
        try:
            self.file_mover.execute(file_path, "plans", "Message processing required")
        except Exception as e:
            print(f"Error handling message: {str(e)}")

    def _handle_standard_processing(self, file_path: str, action_item: Dict[str, Any]):
        """Handle standard processing requests."""
        print(f"Standard processing: {Path(file_path).name}")

        # Standard processing - move to plans for processing
        try:
            self.file_mover.execute(file_path, "plans", "Standard processing")
        except Exception as e:
            print(f"Error in standard processing: {str(e)}")

    def process_pending_approvals(self):
        """Process any pending approval responses."""
        pending_approvals = self.approval_manager.get_pending_approvals()

        print(f"Found {len(pending_approvals)} pending approvals")

        # In a real implementation, this would check for human responses
        # For demo purposes, we'll just show what's pending

    def auto_clean_completed_items(self):
        """Move completed items to Done folder."""
        print("Checking for completed items to move to Done...")

        try:
            result = self.file_mover.move_completed_items("Needs_Action")
            if "completed_files" in result:
                print(f"Moved {len(result['completed_files'])} completed items to Done")
            else:
                print(result.get("message", "No completed items found"))
        except Exception as e:
            print(f"Error in auto clean: {str(e)}")

    def update_dashboard(self):
        """Update the dashboard with current status."""
        print("Updating dashboard...")

        try:
            dashboard_path = self.vault_dir / "Dashboard.md"

            if dashboard_path.exists():
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Update stats in dashboard
                needs_action_count = len(list((self.vault_dir / "Needs_Action").glob("*.md")))
                done_count = len(list((self.vault_dir / "Done").glob("*.md")))
                plans_count = len(list((self.vault_dir / "Plans").glob("*.md")))
                pending_approval_count = len(list((self.vault_dir / "Pending_Approval").glob("*.md")))

                # Update or add stats section
                stats_section = f"""
## System Stats (Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
- **Pending Actions**: {needs_action_count}
- **Completed Items**: {done_count}
- **Active Plans**: {plans_count}
- **Pending Approvals**: {pending_approval_count}
- **Last Processing**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

                # Replace or add stats section
                if "## System Stats" in content:
                    # Replace existing stats section
                    import re
                    content = re.sub(r'## System Stats.*?(?=## |\Z)', stats_section.strip(), content, flags=re.DOTALL)
                else:
                    # Add stats section to the end
                    content += stats_section

                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print("Dashboard updated successfully")
            else:
                print("Dashboard.md not found")

        except Exception as e:
            print(f"Error updating dashboard: {str(e)}")

    def run_cycle(self):
        """Run a single processing cycle."""
        print(f"\n--- Processing Cycle Started at {datetime.now()} ---")

        # Process any new items in Needs_Action
        self.process_needs_action_items()

        # Process any pending approvals
        self.process_pending_approvals()

        # Auto-clean completed items
        self.auto_clean_completed_items()

        # Update dashboard
        self.update_dashboard()

        print(f"--- Processing Cycle Completed at {datetime.now()} ---\n")

    def run_continuous(self, cycle_interval: int = 30):
        """Run the AI Employee continuously."""
        print(f"Starting continuous operation (cycle every {cycle_interval}s)...")

        self.running = True

        # Start the file watcher
        observer = self.start_watcher()

        try:
            while self.running:
                self.run_cycle()
                time.sleep(cycle_interval)
        except KeyboardInterrupt:
            print("\nReceived interrupt signal, shutting down...")
        finally:
            self.running = False
            self.stop_watcher()
            print("AI Employee Controller shutdown complete")

    def run_once(self):
        """Run the AI Employee once for testing."""
        print("Running AI Employee once for testing...")
        self.run_cycle()


def main():
    """Main function to run the AI Employee Controller."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Controller')
    parser.add_argument('--vault-dir', default='./AI_Employee_Vault',
                       help='Vault directory (default: ./AI_Employee_Vault)')
    parser.add_argument('--monitored-dir', default='./watch_input',
                       help='Directory to monitor (default: ./watch_input)')
    parser.add_argument('--continuous', action='store_true',
                       help='Run continuously instead of once')
    parser.add_argument('--interval', type=int, default=30,
                       help='Cycle interval in seconds (default: 30)')

    args = parser.parse_args()

    controller = AIEmployeeController(
        vault_dir=args.vault_dir,
        monitored_dir=args.monitored_dir
    )

    if args.continuous:
        controller.run_continuous(cycle_interval=args.interval)
    else:
        controller.run_once()


if __name__ == "__main__":
    main()