# src/core/state_store.py
"""
Project State Store - Persists project state across runs.
Stores tasks, schedules, and execution history.
"""
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path


class ProjectStateStore:
    """Manages persistent project state using JSON file storage."""
    
    def __init__(self, state_dir: Optional[str] = None):
        """
        Initialize state store.
        
        Args:
            state_dir: Directory to store state files (defaults to project_root/state)
        """
        if state_dir is None:
            project_root = Path(__file__).parent.parent.parent
            state_dir = project_root / "state"
        
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        
        self.state_file = self.state_dir / "project_state.json"
        self.history_file = self.state_dir / "execution_history.json"
        
        # Load or initialize state
        self.state = self._load_state()
        self.history = self._load_history()

    def _load_state(self) -> Dict[str, Any]:
        """Load current state from file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.state_file}, starting fresh")

        # Initialize empty state
        return {
            "issues": {},  # Keyed by source:id
            "scheduled_tasks": {},  # Keyed by task name
            "last_updated": None,
            "metadata": {
                "total_issues_processed": 0,
                "total_tasks_scheduled": 0
            }
        }

    def load_state(self) -> Dict[str, Any]:
        """Load current state from file for update check."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    content = f.read()

                    # Return empty string if file is empty
                    if not content or not content.strip():
                        return ""

                    return json.loads(content)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.state_file}, starting fresh")

        # Initialize empty state
        return {
            "issues": {},  # Keyed by source:id
            "scheduled_tasks": {},  # Keyed by task name
            "last_updated": None,
            "metadata": {
                "total_issues_processed": 0,
                "total_tasks_scheduled": 0
            }
        }
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load execution history from file."""
        if self.history_file.exists():
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {self.history_file}, starting fresh")
        
        return []
    
    def _save_state(self):
        """Persist current state to file."""
        self.state["last_updated"] = datetime.now().isoformat()
        
        with open(self.state_file, "w") as f:
            json.dump(self.state, f, indent=2)
    
    def _save_history(self):
        """Persist execution history to file."""
        with open(self.history_file, "w") as f:
            json.dump(self.history, f, indent=2)
    
    def add_issue(self, issue: Dict[str, Any]):
        """
        Add or update an issue in the state.
        
        Args:
            issue: Issue dict with 'source' and 'id' fields
        """
        key = f"{issue['source']}:{issue['id']}"
        
        self.state["issues"][key] = {
            **issue,
            "added_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.state["metadata"]["total_issues_processed"] += 1
        self._save_state()
    
    def get_issue(self, source: str, issue_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve an issue from state."""
        key = f"{source}:{issue_id}"
        return self.state["issues"].get(key)
    
    def add_scheduled_tasks(self, issue_key: str, tasks: List[Dict[str, Any]]):
        """
        Add scheduled tasks to state.
        
        Args:
            issue_key: Issue identifier (source:id)
            tasks: List of scheduled task dicts
        """
        for task in tasks:
            task_key = f"{issue_key}:{task['task']}"
            
            self.state["scheduled_tasks"][task_key] = {
                "issue": issue_key,
                "task": task["task"],
                "start": task["start"],
                "end": task["end"],
                "duration": task.get("duration"),
                "depends_on": task.get("depends_on", []),
                "scheduled_at": datetime.now().isoformat(),
                "status": "scheduled"  # scheduled, in_progress, completed
            }
        
        self.state["metadata"]["total_tasks_scheduled"] += len(tasks)
        self._save_state()
    
    def get_scheduled_tasks(
        self, 
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get scheduled tasks, optionally filtered by status.
        
        Args:
            status: Filter by status (scheduled, in_progress, completed)
        
        Returns:
            List of task dicts
        """
        tasks = list(self.state["scheduled_tasks"].values())
        
        if status:
            tasks = [t for t in tasks if t.get("status") == status]
        
        return tasks
    
    def update_task_status(self, issue_key: str, task_name: str, status: str):
        """
        Update the status of a scheduled task.
        
        Args:
            issue_key: Issue identifier (source:id)
            task_name: Task name
            status: New status (scheduled, in_progress, completed)
        """
        task_key = f"{issue_key}:{task_name}"
        
        if task_key in self.state["scheduled_tasks"]:
            self.state["scheduled_tasks"][task_key]["status"] = status
            self.state["scheduled_tasks"][task_key]["updated_at"] = datetime.now().isoformat()
            self._save_state()
    
    def log_execution(
        self, 
        action: str, 
        details: Dict[str, Any],
        success: bool = True
    ):
        """
        Log an execution event to history.
        
        Args:
            action: Action name (e.g., 'schedule_tasks', 'send_notification')
            details: Action details
            success: Whether action succeeded
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "success": success,
            "details": details
        }
        
        self.history.append(entry)
        
        # Keep last 1000 entries
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
        
        self._save_history()
    
    def get_history(
        self, 
        action: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get execution history, optionally filtered by action.
        
        Args:
            action: Filter by action name
            limit: Maximum number of entries to return (most recent first)
        
        Returns:
            List of history entries
        """
        history = self.history[::-1]  # Reverse for most recent first
        
        if action:
            history = [h for h in history if h.get("action") == action]
        
        return history[:limit]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the project state."""
        return {
            "total_issues": len(self.state["issues"]),
            "total_scheduled_tasks": len(self.state["scheduled_tasks"]),
            "tasks_by_status": self._count_tasks_by_status(),
            "last_updated": self.state["last_updated"],
            "metadata": self.state["metadata"]
        }
    
    def _count_tasks_by_status(self) -> Dict[str, int]:
        """Count tasks grouped by status."""
        counts = {}
        for task in self.state["scheduled_tasks"].values():
            status = task.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def clear_state(self):
        """Clear all state (use with caution!)."""
        self.state = {
            "issues": {},
            "scheduled_tasks": {},
            "last_updated": None,
            "metadata": {
                "total_issues_processed": 0,
                "total_tasks_scheduled": 0
            }
        }
        self._save_state()
    
    def export_state(self, output_path: str):
        """Export current state to a file."""
        with open(output_path, "w") as f:
            json.dump({
                "state": self.state,
                "history": self.history
            }, f, indent=2)



