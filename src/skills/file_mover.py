"""
File Mover Skill for AI Employee

Moves files between vault folders and maintains audit trail.
"""
import shutil
from pathlib import Path
from typing import Dict, Any, List
from .base_skill import BaseSkill
import os


class FileMover(BaseSkill):
    """Skill to move files between vault folders and update dashboard."""

    def execute(self,
                source_file: str,
                destination_folder: str,
                reason: str = "Manual move",
                update_dashboard: bool = True) -> Dict[str, Any]:
        """
        Move a file from source to destination folder.

        Args:
            source_file: Path to the source file
            destination_folder: Name of the destination folder ('Done', 'Plans', etc.)
            reason: Reason for the move
            update_dashboard: Whether to update the dashboard

        Returns:
            Dictionary with move results
        """
        source_path = Path(source_file)

        # Validate source file exists
        if not source_path.exists():
            return {"success": False, "error": f"Source file does not exist: {source_path}"}

        # Validate destination folder
        dest_folder_map = {
            "done": self.done_dir,
            "plans": self.plans_dir,
            "needs_action": self.needs_action_dir,
            "inbox": self.vault_dir / "Inbox",
            "logs": self.logs_dir,
            "pending_approval": self.pending_approval_dir
        }

        dest_key = destination_folder.lower()
        if dest_key not in dest_folder_map:
            return {
                "success": False,
                "error": f"Invalid destination folder: {destination_folder}. Valid options: {list(dest_folder_map.keys())}"
            }

        destination_dir = dest_folder_map[dest_key]

        # Create destination path
        dest_path = destination_dir / source_path.name

        try:
            # Move the file
            shutil.move(str(source_path), str(dest_path))

            result = {
                "success": True,
                "moved_from": str(source_path),
                "moved_to": str(dest_path),
                "reason": reason,
                "file_size": dest_path.stat().st_size,
                "timestamp": self._get_timestamp()
            }

            # Log the activity
            self.log_activity(
                skill_name="FileMover",
                action="file_moved",
                details={
                    "source": str(source_path),
                    "destination": str(dest_path),
                    "reason": reason,
                    "file_size": result["file_size"]
                }
            )

            # Update dashboard if requested
            if update_dashboard:
                self._update_dashboard_after_move(result)

            return result

        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "attempted_move": {
                    "source": str(source_path),
                    "destination": str(dest_path)
                }
            }

            self.log_activity(
                skill_name="FileMover",
                action="move_failed",
                details={
                    "source": str(source_path),
                    "destination": str(dest_path),
                    "error": str(e)
                }
            )

            return error_result

    def batch_move(self,
                   source_files: List[str],
                   destination_folder: str,
                   reason: str = "Batch move") -> Dict[str, Any]:
        """
        Move multiple files to a destination folder.

        Args:
            source_files: List of source file paths
            destination_folder: Name of the destination folder
            reason: Reason for the moves

        Returns:
            Dictionary with batch move results
        """
        results = {
            "successful_moves": [],
            "failed_moves": [],
            "summary": {
                "total_attempts": len(source_files),
                "successful": 0,
                "failed": 0
            }
        }

        for file_path in source_files:
            result = self.execute(file_path, destination_folder, reason, update_dashboard=False)
            if result["success"]:
                results["successful_moves"].append(result)
            else:
                results["failed_moves"].append(result)

        results["summary"]["successful"] = len(results["successful_moves"])
        results["summary"]["failed"] = len(results["failed_moves"])

        # Update dashboard once after all moves
        if results["successful_moves"]:
            self._update_dashboard_after_batch_move(results)

        return results

    def _update_dashboard_after_move(self, move_result: Dict[str, Any]):
        """Update the dashboard after a file move."""
        try:
            dashboard_path = self.vault_dir / "Dashboard.md"

            if dashboard_path.exists():
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Add move activity to dashboard
                activity_entry = f"\n- {self._get_timestamp()}: Moved '{move_result['moved_from'].split('/')[-1]}' to {move_result['moved_to'].split('/')[-2]} - {move_result['reason']}"

                # Find a good place to insert the activity (after recent activity section if it exists)
                if "Recent Activity" in content:
                    content = content.replace(
                        "Recent Activity",
                        f"Recent Activity{activity_entry}"
                    )
                else:
                    content += activity_entry

                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.log_activity(
                    skill_name="FileMover",
                    action="dashboard_updated",
                    details={
                        "dashboard_path": str(dashboard_path),
                        "activity_added": activity_entry.strip()
                    }
                )

        except Exception as e:
            self.log_activity(
                skill_name="FileMover",
                action="dashboard_update_failed",
                details={"error": str(e)}
            )

    def _update_dashboard_after_batch_move(self, batch_results: Dict[str, Any]):
        """Update the dashboard after a batch move."""
        try:
            dashboard_path = self.vault_dir / "Dashboard.md"

            if dashboard_path.exists():
                with open(dashboard_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Add batch move activity to dashboard
                activity_entry = f"\n- {self._get_timestamp()}: Batch move completed - {batch_results['summary']['successful']} files moved successfully, {batch_results['summary']['failed']} failed"

                if "Recent Activity" in content:
                    content = content.replace(
                        "Recent Activity",
                        f"Recent Activity{activity_entry}"
                    )
                else:
                    content += activity_entry

                with open(dashboard_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        except Exception as e:
            self.log_activity(
                skill_name="FileMover",
                action="dashboard_update_failed",
                details={"error": str(e)}
            )

    def _get_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def move_completed_items(self, source_folder: str = "Needs_Action") -> Dict[str, Any]:
        """
        Move completed items (those with all checkboxes checked) to Done folder.

        Args:
            source_folder: Source folder to check for completed items

        Returns:
            Dictionary with move results
        """
        source_dir = self.vault_dir / source_folder
        if not source_dir.exists():
            return {"success": False, "error": f"Source folder does not exist: {source_dir}"}

        completed_files = []
        for file_path in source_dir.glob("*.md"):
            if self._is_file_completed(file_path):
                completed_files.append(str(file_path))

        if not completed_files:
            return {
                "success": True,
                "message": f"No completed files found in {source_folder}",
                "completed_files": []
            }

        return self.batch_move(completed_files, "done", "Auto-move completed items")

    def _is_file_completed(self, file_path: Path) -> bool:
        """Check if a markdown file has all checkboxes completed."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count unchecked and checked boxes
            unchecked_count = content.count("- [ ]")
            checked_count = content.count("- [x]") + content.count("- [X]")

            # File is considered completed if there are no unchecked boxes
            # and at least some checkboxes exist
            has_checkboxes = (unchecked_count + checked_count) > 0
            all_checked = unchecked_count == 0 and checked_count > 0

            return has_checkboxes and all_checked

        except Exception:
            # If we can't read the file, assume it's not completed
            return False