# src/core/update_check.py

from src.core.state_store import ProjectStateStore

import os
import json
import re
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

from src.core.llm import LLMClient


class UpdateChecker:
    def __init__(self):

        project_root = Path.cwd()
        templates_path = project_root / "src" / "templates"


        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.template = self.env.get_template("update_check_prompt.j2")
        self.llm = LLMClient()
        self.pstate_store = ProjectStateStore()
        self.pstate_store_result = {}

    def check(self, issue_key):
        """checks if issue is already scheduled and returns reply."""
        self.pstate_store_result = self.pstate_store.load_state()

        prompt = self.template.render(issue=issue_key, pstate_store = self.pstate_store_result)
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




