# src/core/plan_validation.py
import os
import json
import re
from jinja2 import Environment, FileSystemLoader

from .llm import LLMClient


class PlanValidator:
    def __init__(self):
        templates_path = os.path.join(
            os.path.dirname(__file__), "..", "templates"
        )
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.template = self.env.get_template("validation_prompt.j2")
        self.llm = LLMClient()

    def validate(self, tasks):
        """Validate task plan and return a decision dict."""
        prompt = self.template.render(tasks=tasks)
        raw = self.llm.run(prompt)

        cleaned = self._extract_json(raw)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print("LLM validation output was not valid JSON:\n", raw)
            raise

    @staticmethod
    def _extract_json(text: str) -> str:
        t = text.strip()

        if t.startswith("```"):
            t = re.sub(r"^```[a-zA-Z0-9_]*", "", t).strip()
            if "```" in t:
                t = t.split("```", 1)[0].strip()

        return t