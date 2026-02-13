"""
Base Skill Class for AI Employee Agent Skills

Defines the common interface and functionality for all agent skills.
"""
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class BaseSkill(ABC):
    """Base class for all AI Employee skills."""

    def __init__(self, vault_dir: str = "./AI_Employee_Vault"):
        self.vault_dir = Path(vault_dir)
        self.logs_dir = self.vault_dir / "Logs"
        self.needs_action_dir = self.vault_dir / "Needs_Action"
        self.done_dir = self.vault_dir / "Done"
        self.plans_dir = self.vault_dir / "Plans"
        self.pending_approval_dir = self.vault_dir / "Pending_Approval"

        # Create directories if they don't exist
        for dir_path in [self.logs_dir, self.needs_action_dir, self.done_dir,
                        self.plans_dir, self.pending_approval_dir]:
            dir_path.mkdir(exist_ok=True)

    def log_activity(self, skill_name: str, action: str, details: Dict[str, Any]):
        """Log activity to the logs directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "skill": skill_name,
            "action": action,
            "details": details
        }

        log_file = self.logs_dir / f"log_{timestamp}.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, indent=2, ensure_ascii=False)

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the skill with given parameters."""
        pass