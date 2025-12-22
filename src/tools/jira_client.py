# src/tools/jira_client.py
"""
Jira API client for fetching and updating issues.
Uses Jira Cloud REST API v3.
"""
import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH)


class JiraClient:
    """Client for Jira Cloud REST API."""
    
    def __init__(self):
        self.base_url = os.getenv("JIRA_URL", "").rstrip("/")
        self.email = os.getenv("JIRA_EMAIL", "")
        self.api_token = os.getenv("JIRA_API_TOKEN", "")
        
        if not all([self.base_url, self.email, self.api_token]):
            raise ValueError(
                "Jira configuration incomplete. Please set JIRA_URL, "
                "JIRA_EMAIL, and JIRA_API_TOKEN in .env"
            )
        
        self.auth = (self.email, self.api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
    
    def get_issues(
        self, 
        project_key: str, 
        max_results: int = 50,
        jql: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch issues from a Jira project.
        
        Args:
            project_key: Jira project key (e.g., "PROJ")
            max_results: Maximum number of issues to return
            jql: Optional JQL query to filter issues
        
        Returns:
            List of issue dictionaries with normalized fields
        """
        # Build JQL query
        if jql is None:
            # Default: fetch open issues from project, ordered by priority
            jql = (
                f'project = "{project_key}" '
                f'AND status != Done '
                f'ORDER BY priority DESC, created DESC'
            )
        
        url = f"{self.base_url}/rest/api/3/search/jql"
        params = {
            "jql": jql,
            "maxResults": max_results,
            "fields": "summary,description,status,priority,assignee,created,updated"
        }
        
        try:
            response = requests.get(
                url,
                auth=self.auth,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Normalize issues to consistent format
            issues = []
            for issue in data.get("issues", []):
                fields = issue.get("fields", {})
                
                # Extract assignee name if present
                assignee = None
                if fields.get("assignee"):
                    assignee = fields["assignee"].get("displayName", "Unassigned")
                
                # Extract priority
                priority = "Medium"  # default
                if fields.get("priority"):
                    priority = fields["priority"].get("name", "Medium")
                
                issues.append({
                    "key": issue.get("key", ""),
                    "title": fields.get("summary", ""),
                    "body": fields.get("description", "") or "",
                    "status": fields.get("status", {}).get("name", "Unknown"),
                    "priority": priority,
                    "assignee": assignee,
                    "created": fields.get("created", ""),
                    "updated": fields.get("updated", ""),
                    "url": f"{self.base_url}/browse/{issue.get('key', '')}"
                })
            
            return issues
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch Jira issues: {str(e)}")
    
    def update_issue(
        self, 
        issue_key: str, 
        fields: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a Jira issue.
        
        Args:
            issue_key: Issue key (e.g., "PROJ-123")
            fields: Dictionary of fields to update
        
        Returns:
            Response data from Jira
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        payload = {"fields": fields}
        
        try:
            response = requests.put(
                url,
                auth=self.auth,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "message": f"Updated {issue_key}"}
            
        except requests.RequestException as e:
            raise Exception(f"Failed to update Jira issue {issue_key}: {str(e)}")
    
    def add_comment(self, issue_key: str, comment: str) -> Dict[str, Any]:
        """
        Add a comment to a Jira issue.
        
        Args:
            issue_key: Issue key (e.g., "PROJ-123")
            comment: Comment text
        
        Returns:
            Response data from Jira
        """
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/comment"
        
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment
                            }
                        ]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "message": f"Added comment to {issue_key}"}
            
        except requests.RequestException as e:
            raise Exception(f"Failed to add comment to {issue_key}: {str(e)}")
    
    def transition_issue(
        self, 
        issue_key: str, 
        transition_name: str
    ) -> Dict[str, Any]:
        """
        Transition a Jira issue to a new status.
        
        Args:
            issue_key: Issue key (e.g., "PROJ-123")
            transition_name: Target transition name (e.g., "In Progress", "Done")
        
        Returns:
            Response data from Jira
        """
        # First, get available transitions
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}/transitions"
        
        try:
            response = requests.get(
                url,
                auth=self.auth,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            transitions = response.json().get("transitions", [])
            
            # Find matching transition
            transition_id = None
            for t in transitions:
                if t["name"].lower() == transition_name.lower():
                    transition_id = t["id"]
                    break
            
            if not transition_id:
                available = [t["name"] for t in transitions]
                raise Exception(
                    f"Transition '{transition_name}' not available for {issue_key}. "
                    f"Available: {', '.join(available)}"
                )
            
            # Perform transition
            payload = {"transition": {"id": transition_id}}
            response = requests.post(
                url,
                auth=self.auth,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return {
                "success": True, 
                "message": f"Transitioned {issue_key} to {transition_name}"
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to transition {issue_key}: {str(e)}")



