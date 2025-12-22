import json
from src.core.llm_factory import LLMFactory

ALLOWED_TOOLS = [
    "tasks_breakdown",
    "tasks_breakdown_multi",
    "plan_validation",
    "tasks_schedule",
    "jira_add_comment",
    "slack_notify_scheduled_tasks",
    "stop"
]

class ReasoningController:
    def __init__(self):
        clients = LLMFactory.create_all_available_clients()


        self.llm = clients["github"]

    def decide(self, context: dict) -> dict:
        prompt = f"""
        You are a reasoning controller for an autonomous task management agent.

        Your goal is to decide the NEXT best action based on the current state.
        You should reason step-by-step, but ONLY output the final decision as JSON.

        Guidelines:
        - If no tasks exist yet, breaking the issue down into tasks is usually the right first step.
        - If tasks exist and are ready, scheduling them is usually the next step.
        - Do NOT repeat the same action if it has already been successfully performed.
        - If nothing meaningful can be done next, stop.

        Allowed tools:
        - tasks_breakdown
        - tasks_schedule
        - stop

        Current context (JSON):
        {json.dumps(context, indent=2)}

        Return ONLY valid JSON in this exact format:
        {{
        "actions": [
            {{"tool": "<tool_name>"}}
        ],
        "done": false
        }}
        """


        response = self.llm.run(prompt)

        return json.loads(response)