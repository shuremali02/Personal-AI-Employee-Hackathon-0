"""
File Processor Skill for AI Employee

Reads files from Needs_Action, parses content and metadata, and determines appropriate action.
"""
import os
import re
from pathlib import Path
from typing import Dict, Any, List
from .base_skill import BaseSkill


class FileProcessor(BaseSkill):
    """Skill to process files from Needs_Action directory."""

    def execute(self, file_pattern: str = "*.md", max_files: int = 10) -> Dict[str, Any]:
        """
        Process files from Needs_Action directory.

        Args:
            file_pattern: Pattern to match files (default: *.md)
            max_files: Maximum number of files to process at once

        Returns:
            Dictionary with processing results
        """
        results = {
            "processed_files": [],
            "actions_determined": [],
            "errors": [],
            "summary": {}
        }

        # Find files to process
        files_to_process = list(self.needs_action_dir.glob(file_pattern))

        # Limit the number of files to process
        files_to_process = files_to_process[:max_files]

        for file_path in files_to_process:
            try:
                # Parse the file
                parsed_data = self._parse_file(file_path)

                # Determine appropriate action
                action = self._determine_action(parsed_data)

                # Add to results
                results["processed_files"].append(str(file_path))
                results["actions_determined"].append({
                    "file": str(file_path),
                    "action": action,
                    "parsed_data": parsed_data
                })

                # Log the activity
                self.log_activity(
                    skill_name="FileProcessor",
                    action="file_processed",
                    details={
                        "file": str(file_path),
                        "action": action,
                        "parsed_keys": list(parsed_data.keys()) if parsed_data else []
                    }
                )

            except Exception as e:
                error_msg = f"Error processing {file_path}: {str(e)}"
                results["errors"].append(error_msg)
                self.log_activity(
                    skill_name="FileProcessor",
                    action="error",
                    details={"file": str(file_path), "error": str(e)}
                )

        # Summary
        results["summary"] = {
            "total_files_found": len(list(self.needs_action_dir.glob(file_pattern))),
            "files_processed": len(results["processed_files"]),
            "successful": len(results["processed_files"]) - len(results["errors"]),
            "errors": len(results["errors"])
        }

        return results

    def _parse_file(self, file_path: Path) -> Dict[str, Any]:
        """Parse the content and metadata of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter if present
            frontmatter = self._extract_frontmatter(content)

            # Extract content without frontmatter
            content_body = self._remove_frontmatter(content)

            # Extract key information
            extracted_info = {
                "filename": file_path.name,
                "filepath": str(file_path),
                "size": file_path.stat().st_size,
                "frontmatter": frontmatter,
                "content_preview": content_body[:500],  # First 500 chars
                "word_count": len(content.split()),
                "has_checkboxes": bool(re.search(r'- \[ \]', content) or re.search(r'- \[x\]', content, re.IGNORECASE)),
                "has_links": bool(re.search(r'\[.*\]\(.*\)', content)),
                "headers": self._extract_headers(content_body)
            }

            return extracted_info
        except Exception as e:
            return {
                "filename": file_path.name,
                "filepath": str(file_path),
                "error": str(e)
            }

    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        """Extract YAML frontmatter from content."""
        import yaml

        # Look for YAML frontmatter between --- delimiters
        if content.startswith("---"):
            try:
                # Split on the closing ---
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    frontmatter_content = parts[1]
                    return yaml.safe_load(frontmatter_content) or {}
            except Exception:
                pass

        return {}

    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content."""
        if content.startswith("---"):
            try:
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            except Exception:
                pass

        return content

    def _extract_headers(self, content: str) -> List[str]:
        """Extract headers from markdown content."""
        headers = []
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                header = line.strip()
                headers.append(header)
                if len(headers) >= 5:  # Limit to first 5 headers
                    break
        return headers

    def _determine_action(self, parsed_data: Dict[str, Any]) -> str:
        """Determine the appropriate action based on parsed data."""
        # Check frontmatter for explicit action
        frontmatter = parsed_data.get("frontmatter", {})

        if "action_required" in frontmatter:
            action = frontmatter["action_required"]
            # Normalize the action to match our expected values
            if "create_plan" in action.lower():
                return "create_plan"
            elif "send_to_approval" in action.lower() or "approval" in action.lower():
                return "send_to_approval"
            elif "urgent" in action.lower():
                return "urgent_processing"
            else:
                return action.lower()

        if "status" in frontmatter and frontmatter["status"] == "pending_approval":
            return "send_to_approval"

        # Check for approval-related fields in frontmatter
        if any(key in frontmatter for key in ["budget", "approval_needed", "requires_approval", "amount_requested"]):
            return "send_to_approval"

        # Check content for specific patterns
        content_preview = parsed_data.get("content_preview", "").lower()

        if "urgent" in content_preview or "asap" in content_preview or "immediate" in content_preview:
            return "urgent_processing"

        if "approval" in content_preview or "approve" in content_preview or "escalate" in content_preview:
            return "send_to_approval"

        if "plan" in content_preview or "todo" in content_preview or "task" in content_preview:
            return "create_plan"

        if "email" in content_preview or "contact" in content_preview or "message" in content_preview:
            return "send_message"

        # Check for budget or financial terms that might need approval
        if any(term in content_preview for term in ["budget", "$", "funds", "spend", "purchase", "expense"]):
            return "send_to_approval"

        # Default action
        return "standard_processing"