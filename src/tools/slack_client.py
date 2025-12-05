# src/tools/slack_client.py
"""
Slack API client for sending notifications.
"""
import os
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH)


class SlackClient:
    """Client for Slack Web API."""
    
    def __init__(self):
        self.bot_token = os.getenv("SLACK_BOT_TOKEN", "")
        self.default_channel = os.getenv("SLACK_CHANNEL", "#general")
        
        if not self.bot_token:
            raise ValueError(
                "Slack configuration incomplete. Please set SLACK_BOT_TOKEN in .env"
            )
        
        self.headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
    
    def send_message(
        self, 
        text: str, 
        channel: Optional[str] = None,
        blocks: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Send a message to a Slack channel.
        
        Args:
            text: Message text (also used as fallback for blocks)
            channel: Channel to send to (defaults to SLACK_CHANNEL from .env)
            blocks: Optional Block Kit blocks for rich formatting
        
        Returns:
            Response data from Slack API
        """
        url = "https://slack.com/api/chat.postMessage"
        
        channel = channel or self.default_channel
        
        payload = {
            "channel": channel,
            "text": text
        }
        
        if blocks:
            payload["blocks"] = blocks
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("ok"):
                error = data.get("error", "Unknown error")
                raise Exception(f"Slack API error: {error}")
            
            return {
                "success": True,
                "channel": channel,
                "timestamp": data.get("ts")
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to send Slack message: {str(e)}")
    
    def send_task_schedule_notification(
        self,
        issue_source: str,
        issue_title: str,
        tasks: List[Dict[str, Any]],
        channel: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a formatted notification about scheduled tasks.
        
        Args:
            issue_source: Source system (e.g., "GitHub", "Jira")
            issue_title: Title of the issue
            tasks: List of scheduled tasks
            channel: Channel to send to
        
        Returns:
            Response data from Slack API
        """
        # Create rich formatted message using Block Kit
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🎯 Tasks Scheduled from {issue_source}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Issue:* {issue_title}"
                }
            },
            {
                "type": "divider"
            }
        ]
        
        # Add each task
        for i, task in enumerate(tasks, 1):
            task_text = (
                f"*{i}. {task['task']}*\n"
                f"⏰ {self._format_time(task['start'])} → {self._format_time(task['end'])}\n"
                f"📊 Duration: {task.get('duration', 'N/A')} hours"
            )
            
            if task.get("depends_on"):
                deps = ", ".join(task["depends_on"])
                task_text += f"\n🔗 Depends on: {deps}"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": task_text
                }
            })
        
        # Add footer
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Scheduled {len(tasks)} task(s) | {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                }
            ]
        })
        
        # Fallback text for notifications
        fallback_text = (
            f"Tasks scheduled from {issue_source}: {issue_title} "
            f"({len(tasks)} task(s))"
        )
        
        return self.send_message(
            text=fallback_text,
            channel=channel,
            blocks=blocks
        )
    
    def send_error_notification(
        self,
        error_message: str,
        context: Optional[str] = None,
        channel: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an error notification.
        
        Args:
            error_message: Error message
            context: Additional context
            channel: Channel to send to
        
        Returns:
            Response data from Slack API
        """
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "⚠️ Agent Error",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Error:* {error_message}"
                }
            }
        ]
        
        if context:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Context:* {context}"
                }
            })
        
        fallback_text = f"Agent Error: {error_message}"
        
        return self.send_message(
            text=fallback_text,
            channel=channel,
            blocks=blocks
        )
    
    @staticmethod
    def _format_time(iso_time: str) -> str:
        """Format ISO timestamp to readable format."""
        try:
            dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
            return dt.strftime("%b %d, %H:%M")
        except Exception:
            return iso_time

