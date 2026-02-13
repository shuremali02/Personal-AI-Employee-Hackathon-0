"""
Approval Manager Skill for AI Employee

Handles human-in-the-loop workflows and manages approval status tracking.
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
from .base_skill import BaseSkill
import uuid
from datetime import datetime


class ApprovalManager(BaseSkill):
    """Skill to manage approval workflows and human-in-the-loop processes."""

    def execute(self,
                action_type: str,
                description: str,
                requester: str = "AI Employee",
                urgency: str = "normal",
                required_approver: str = "human_supervisor",
                additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create an approval request for human intervention.

        Args:
            action_type: Type of action requiring approval
            description: Description of the action needing approval
            requester: Who is requesting the approval
            urgency: Urgency level (low, normal, high, urgent)
            required_approver: Who needs to approve this
            additional_context: Additional context for the approval

        Returns:
            Dictionary with approval request details
        """
        approval_id = f"APPROVAL_{uuid.uuid4().hex[:8]}_{action_type.replace(' ', '_').replace('/', '_')}"

        # Create approval request structure
        approval_data = {
            "id": approval_id,
            "action_type": action_type,
            "description": description,
            "requester": requester,
            "urgency": urgency,
            "required_approver": required_approver,
            "status": "pending",
            "requested_at": datetime.now().isoformat(),
            "expires_at": self._calculate_expiry(urgency),
            "additional_context": additional_context or {},
            "approver_response": None,
            "response_at": None
        }

        # Create markdown file for approval request
        approval_content = self._generate_approval_markdown(approval_data)

        # Save to pending approval directory
        approval_filename = f"{approval_id}.md"
        approval_path = self.pending_approval_dir / approval_filename

        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        # Log the activity
        self.log_activity(
            skill_name="ApprovalManager",
            action="approval_request_created",
            details={
                "approval_id": approval_id,
                "action_type": action_type,
                "urgency": urgency,
                "requester": requester,
                "save_path": str(approval_path)
            }
        )

        approval_data["saved_path"] = str(approval_path)
        approval_data["content"] = approval_content

        return approval_data

    def _generate_approval_markdown(self, approval_data: Dict[str, Any]) -> str:
        """Generate markdown content for the approval request."""
        context_str = ""
        if approval_data["additional_context"]:
            context_str = "\n## Additional Context\n"
            for key, value in approval_data["additional_context"].items():
                context_str += f"- **{key}**: {value}\n"

        content = f"""---
title: "Approval Request: {approval_data['action_type']}"
id: "{approval_data['id']}"
action_type: "{approval_data['action_type']}"
requester: "{approval_data['requester']}"
required_approver: "{approval_data['required_approver']}"
urgency: "{approval_data['urgency']}"
status: "{approval_data['status']}"
requested_at: "{approval_data['requested_at']}"
expires_at: "{approval_data['expires_at']}"
---

# Approval Request: {approval_data['action_type']}

**Request ID:** `{approval_data['id']}`
**Requested by:** {approval_data['requester']}
**Required Approver:** {approval_data['required_approver']}
**Urgency:** {approval_data['urgency']}
**Status:** {approval_data['status']}
**Requested at:** {approval_data['requested_at']}
**Expires at:** {approval_data['expires_at']}

## Description
{approval_data['description']}

{context_str}

## Approval Options
- [ ] **Approve** - Allow the action to proceed
- [ ] **Reject** - Deny the action
- [ ] **Escalate** - Send to higher authority

## Instructions for Approver
1. Review the details above carefully
2. Consider the potential impacts of this action
3. Make your decision using the checkboxes above
4. Add any comments or concerns in the space below
5. The AI Employee will process your response automatically

## Comments
_Add your comments here_

---
**Note:** This request will expire on {approval_data['expires_at']} if no action is taken.
"""

        return content

    def _calculate_expiry(self, urgency: str) -> str:
        """Calculate expiry time based on urgency."""
        from datetime import datetime, timedelta

        if urgency == "urgent":
            expiry = datetime.now() + timedelta(hours=2)
        elif urgency == "high":
            expiry = datetime.now() + timedelta(hours=8)
        elif urgency == "low":
            expiry = datetime.now() + timedelta(days=7)
        else:  # normal
            expiry = datetime.now() + timedelta(days=1)

        return expiry.isoformat()

    def process_approval_response(self, approval_id: str, response: str, approver: str) -> Dict[str, Any]:
        """
        Process an approval response from a human approver.

        Args:
            approval_id: ID of the approval request
            response: Response from approver ('approve', 'reject', 'escalate')
            approver: Who provided the response

        Returns:
            Dictionary with processing results
        """
        approval_path = self.pending_approval_dir / f"{approval_id}.md"

        if not approval_path.exists():
            return {"success": False, "error": f"Approval request {approval_id} not found"}

        # Update the approval status in the file
        with open(approval_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update status and add response information
        updated_content = self._update_approval_response(content, response, approver)

        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        # Create response record
        response_record = {
            "approval_id": approval_id,
            "response": response,
            "approver": approver,
            "responded_at": datetime.now().isoformat(),
            "original_path": str(approval_path),
            "new_status": response
        }

        # Move the approval file to appropriate location based on response
        if response == "approve":
            new_path = self.done_dir / f"APPROVED_{approval_id}.md"
        elif response == "reject":
            new_path = self.done_dir / f"REJECTED_{approval_id}.md"
        else:  # escalate
            new_path = self.needs_action_dir / f"ESCALATED_{approval_id}.md"

        import shutil
        shutil.move(str(approval_path), str(new_path))

        response_record["final_path"] = str(new_path)

        # Log the activity
        self.log_activity(
            skill_name="ApprovalManager",
            action="approval_response_processed",
            details={
                "approval_id": approval_id,
                "response": response,
                "approver": approver,
                "final_path": str(new_path)
            }
        )

        return response_record

    def _update_approval_response(self, content: str, response: str, approver: str) -> str:
        """Update the approval file with response information."""
        import re

        # Update the status in frontmatter
        content = re.sub(r'(status: )"\w+"', rf'\g<1>"{response}"', content)

        # Update checkboxes based on response
        if response == "approve":
            content = content.replace("- [ ] **Approve**", "- [x] **Approve**")
        elif response == "reject":
            content = content.replace("- [ ] **Reject**", "- [x] **Reject**")
        elif response == "escalate":
            content = content.replace("- [ ] **Escalate**", "- [x] **Escalate**")

        # Add response information to the bottom
        response_section = f"""

## Response Information
- **Response**: {response.upper()}
- **Approver**: {approver}
- **Timestamp**: {datetime.now().isoformat()}
- **Processed by**: ApprovalManager Skill

---

*This approval request has been processed and moved to the appropriate folder.*
"""

        return content + response_section

    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Get a list of all pending approval requests."""
        pending_approvals = []

        for approval_file in self.pending_approval_dir.glob("APPROVAL_*.md"):
            try:
                with open(approval_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract basic info (in a real implementation, you'd use proper YAML parsing)
                import re

                approval_info = {
                    "id": approval_file.stem,
                    "filename": approval_file.name,
                    "size": approval_file.stat().st_size,
                    "modified": datetime.fromtimestamp(approval_file.stat().st_mtime).isoformat()
                }

                # Extract urgency if mentioned in content
                urgency_match = re.search(r'urgency: "([^"]*)"', content)
                if urgency_match:
                    approval_info["urgency"] = urgency_match.group(1)

                # Extract action type if mentioned
                action_match = re.search(r'action_type: "([^"]*)"', content)
                if action_match:
                    approval_info["action_type"] = action_match.group(1)

                pending_approvals.append(approval_info)

            except Exception as e:
                self.log_activity(
                    skill_name="ApprovalManager",
                    action="pending_approval_read_error",
                    details={"file": str(approval_file), "error": str(e)}
                )

        return pending_approvals

    def auto_expire_approvals(self) -> Dict[str, Any]:
        """Automatically expire old approval requests."""
        from datetime import datetime
        expired_count = 0
        processed_files = []

        for approval_file in self.pending_approval_dir.glob("APPROVAL_*.md"):
            try:
                # Check if the file has expired by reading its content
                with open(approval_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract expiration time
                import re
                expires_match = re.search(r'expires_at: "([^"]*)"', content)
                if expires_match:
                    expires_at = datetime.fromisoformat(expires_match.group(1).replace('Z', '+00:00'))
                    if datetime.now(datetime.timezone.utc) > expires_at:
                        # Expire this approval
                        expired_approval = self._expire_approval(approval_file)
                        processed_files.append(expired_approval)
                        expired_count += 1

            except Exception as e:
                self.log_activity(
                    skill_name="ApprovalManager",
                    action="auto_expire_error",
                    details={"file": str(approval_file), "error": str(e)}
                )

        result = {
            "expired_count": expired_count,
            "processed_files": processed_files,
            "timestamp": datetime.now().isoformat()
        }

        self.log_activity(
            skill_name="ApprovalManager",
            action="auto_expire_run",
            details=result
        )

        return result

    def _expire_approval(self, approval_file: Path) -> Dict[str, Any]:
        """Expire a single approval request."""
        # Read the content
        with open(approval_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update to show it expired
        expired_content = content + f"""

## Expiration Notice
- **Status**: EXPIRED
- **Expired at**: {datetime.now().isoformat()}
- **Reason**: No response received within required timeframe

---

*This approval request has expired and been moved to the Done folder.*
"""

        # Create new file in Done folder with expired status
        expired_path = self.done_dir / f"EXPIRED_{approval_file.name}"
        with open(expired_path, 'w', encoding='utf-8') as f:
            f.write(expired_content)

        # Remove the original pending file
        approval_file.unlink()

        return {
            "original_file": str(approval_file),
            "expired_file": str(expired_path),
            "status": "expired"
        }