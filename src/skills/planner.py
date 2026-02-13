"""
Planner Skill for AI Employee

Creates structured plan files based on input and manages progress tracking.
"""
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from .base_skill import BaseSkill
import uuid


class Planner(BaseSkill):
    """Skill to create structured plan files and track progress."""

    def execute(self,
                plan_title: str,
                objectives: List[str],
                tasks: List[Dict[str, str]] = None,
                dependencies: List[Dict[str, str]] = None,
                save_to_plans: bool = True,
                assignee: str = "AI Employee") -> Dict[str, Any]:
        """
        Create a structured plan with objectives, tasks, and progress tracking.

        Args:
            plan_title: Title for the plan
            objectives: List of objectives to achieve
            tasks: List of tasks with description and priority
            dependencies: List of task dependencies
            save_to_plans: Whether to save the plan to Plans directory
            assignee: Who is responsible for the plan

        Returns:
            Dictionary with plan details
        """
        plan_id = f"PLAN_{uuid.uuid4().hex[:8]}_{plan_title.replace(' ', '_').replace('/', '_')}"

        # Create plan structure
        plan_data = {
            "id": plan_id,
            "title": plan_title,
            "created_at": datetime.now().isoformat(),
            "assignee": assignee,
            "status": "draft",
            "progress": 0,
            "objectives": objectives,
            "tasks": [],
            "dependencies": dependencies or [],
            "completed_tasks": 0,
            "total_tasks": 0
        }

        # Process tasks
        if tasks:
            processed_tasks = []
            for i, task in enumerate(tasks):
                task_entry = {
                    "id": f"task_{i+1}",
                    "description": task.get("description", f"Task {i+1}"),
                    "priority": task.get("priority", "medium"),
                    "status": "pending",
                    "estimated_time": task.get("estimated_time", "30m"),
                    "depends_on": task.get("depends_on", []),
                    "completed": False,
                    "completed_at": None
                }
                processed_tasks.append(task_entry)

            plan_data["tasks"] = processed_tasks
            plan_data["total_tasks"] = len(processed_tasks)

        # Create markdown representation
        plan_content = self._generate_plan_markdown(plan_data)

        # Save to plans directory if requested
        saved_path = None
        if save_to_plans:
            plan_filename = f"{plan_id}.md"
            plan_path = self.plans_dir / plan_filename

            with open(plan_path, 'w', encoding='utf-8') as f:
                f.write(plan_content)

            saved_path = str(plan_path)
            plan_data["saved_path"] = saved_path

        # Log the activity
        self.log_activity(
            skill_name="Planner",
            action="plan_created",
            details={
                "plan_id": plan_id,
                "title": plan_title,
                "tasks_count": len(plan_data.get("tasks", [])),
                "objectives_count": len(objectives),
                "saved_path": saved_path
            }
        )

        plan_data["content"] = plan_content

        return plan_data

    def _generate_plan_markdown(self, plan_data: Dict[str, Any]) -> str:
        """Generate markdown content for the plan."""
        content = f"""---
title: "{plan_data['title']}"
id: "{plan_data['id']}"
created: "{plan_data['created_at']}"
assignee: "{plan_data['assignee']}"
status: "{plan_data['status']}"
progress: {plan_data['progress']}
total_tasks: {plan_data['total_tasks']}
completed_tasks: {plan_data['completed_tasks']}
---

# {plan_data['title']}

**Plan ID:** `{plan_data['id']}`
**Created:** {plan_data['created_at']}
**Assignee:** {plan_data['assignee']}
**Status:** {plan_data['status']}
**Progress:** {plan_data['progress']}% ({plan_data['completed_tasks']}/{plan_data['total_tasks']})

## Objectives
"""

        for i, objective in enumerate(plan_data['objectives'], 1):
            content += f"\n{i}. {objective}\n"

        content += "\n## Tasks\n"

        for i, task in enumerate(plan_data.get('tasks', []), 1):
            status_check = "[x]" if task['completed'] else "[ ]"
            content += f"\n- {status_check} **{task['description']}** (Priority: {task['priority']})\n"
            if task['depends_on']:
                content += f"  - Depends on: {', '.join(task['depends_on'])}\n"
            if task['completed_at']:
                content += f"  - Completed: {task['completed_at']}\n"

        if plan_data['dependencies']:
            content += "\n## Dependencies\n"
            for dep in plan_data['dependencies']:
                content += f"- {dep.get('from', 'Unknown')} → {dep.get('to', 'Unknown')}\n"

        content += f"""

## Progress Tracking
- [ ] Initial plan review
- [ ] Task assignments confirmed
- [ ] First milestone achieved
- [ ] Mid-plan review
- [ ] Final review and completion

## Notes
_Add any additional notes or updates here_

_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
"""

        return content

    def update_task_status(self, plan_id: str, task_id: str, completed: bool = True) -> Dict[str, Any]:
        """
        Update the status of a specific task in a plan.

        Args:
            plan_id: ID of the plan
            task_id: ID of the task to update
            completed: Whether the task is completed

        Returns:
            Updated plan data
        """
        plan_path = self.plans_dir / f"{plan_id}.md"

        if not plan_path.exists():
            return {"error": f"Plan {plan_id} not found"}

        # Read existing plan
        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update the task status in the markdown
        if completed:
            content = content.replace(f"- [ ] **{task_id}", f"- [x] **{task_id}")
        else:
            content = content.replace(f"- [x] **{task_id}", f"- [ ] **{task_id}")

        # Update the plan file
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update plan data
        plan_data = self._load_plan_data(plan_path)
        for task in plan_data.get('tasks', []):
            if task['id'] == task_id:
                task['completed'] = completed
                task['completed_at'] = datetime.now().isoformat() if completed else None
                break

        # Recalculate progress
        completed_tasks = sum(1 for t in plan_data.get('tasks', []) if t.get('completed', False))
        total_tasks = len(plan_data.get('tasks', []))
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        plan_data['completed_tasks'] = completed_tasks
        plan_data['progress'] = round(progress, 2)

        # Update the plan file with new progress
        self._update_plan_progress(plan_path, plan_data)

        self.log_activity(
            skill_name="Planner",
            action="task_updated",
            details={
                "plan_id": plan_id,
                "task_id": task_id,
                "completed": completed,
                "new_progress": plan_data['progress']
            }
        )

        return plan_data

    def _load_plan_data(self, plan_path: Path) -> Dict[str, Any]:
        """Load plan data from markdown file."""
        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple extraction of key data (in practice, you'd want more robust parsing)
        plan_data = {"tasks": [], "objectives": []}

        # Count tasks
        pending_tasks = content.count("- [ ] ")
        completed_tasks = content.count("- [x] ")
        total_tasks = pending_tasks + completed_tasks

        plan_data["completed_tasks"] = completed_tasks
        plan_data["total_tasks"] = total_tasks
        plan_data["progress"] = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        return plan_data

    def _update_plan_progress(self, plan_path: Path, plan_data: Dict[str, Any]):
        """Update progress information in the plan file."""
        with open(plan_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace progress line
        import re
        content = re.sub(
            r'\*\*Progress:\*\* \d+%\s+\(\d+/\d+\)',
            f"**Progress:** {plan_data['progress']}% ({plan_data['completed_tasks']}/{plan_data['total_tasks']})",
            content
        )

        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)