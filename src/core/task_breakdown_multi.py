# src/core/task_breakdown_multi.py
"""
Enhanced task breakdown using multi-agent LLM orchestrator.
"""
import os
import json
import re
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader

from .llm_factory import LLMFactory


class TaskBreakdownMulti:
    """Task breakdown using multi-agent orchestrator."""
    
    def __init__(self, strategy: str = "specialized"):
        """
        Initialize task breakdown with multi-agent support.
        
        Args:
            strategy: Orchestration strategy (ensemble, specialized, fallback, single)
        """
        templates_path = os.path.join(
            os.path.dirname(__file__), "..", "templates"
        )
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.template = self.env.get_template("breakdown_prompt.j2")
        
        # Create multi-agent orchestrator
        self.orchestrator = LLMFactory.create_orchestrator(strategy=strategy)
        self.strategy = strategy
    
    def breakdown(self, issue_text: str) -> List[Dict[str, Any]]:
        """
        Break down issue into tasks using multi-agent orchestrator.
        
        Args:
            issue_text: Issue text to break down
        
        Returns:
            List of task dictionaries
        """
        prompt = self.template.render(issue=issue_text)
        
        # Generate using orchestrator
        result = self.orchestrator.generate(prompt, task_type="breakdown")
        
        if not result.get("success"):
            error_msg = result.get("error", "Unknown error")
            print(f"❌ Multi-agent generation failed: {error_msg}")
            raise Exception(f"LLM generation failed: {error_msg}")
        
        raw = result["content"]
        
        # Log which LLM was used
        provider = result.get("provider_used", "Unknown")
        model = result.get("model_used", "Unknown")
        cost = result.get("cost", 0.0)
        latency = result.get("latency_ms", 0.0)
        
        print(f"🤖 Used: {provider} ({model})")
        print(f"💰 Cost: ${cost:.6f} | ⏱️  Latency: {latency:.0f}ms")
        
        if self.strategy == "ensemble":
            metadata = result.get("metadata", {})
            print(f"📊 Ensemble: {metadata.get('successful_count', 0)}/{metadata.get('successful_count', 0) + metadata.get('failed_count', 0)} LLMs succeeded")
        
        # Parse JSON response
        cleaned = self._extract_json(raw)
        
        try:
            tasks = json.loads(cleaned)
            print(f"✅ Parsed {len(tasks)} tasks successfully")
            return tasks
        except json.JSONDecodeError:
            # Last resort: try first [ ... ] slice
            start = cleaned.find("[")
            end = cleaned.rfind("]")
            if start != -1 and end != -1:
                snippet = cleaned[start:end + 1]
                tasks = json.loads(snippet)
                print(f"✅ Parsed {len(tasks)} tasks (with cleanup)")
                return tasks
            
            # If still failing, show raw output
            print("❌ LLM output was not valid JSON:\n", raw)
            raise
    
    def get_metrics(self) -> List[Dict[str, Any]]:
        """Get performance metrics from all LLMs."""
        return self.orchestrator.get_all_metrics()
    
    def reset_metrics(self):
        """Reset metrics for all LLMs."""
        self.orchestrator.reset_all_metrics()
    
    @staticmethod
    def _extract_json(text: str) -> str:
        """Strip code fences / extra text, keep JSON part."""
        t = text.strip()
        
        # Remove ```json ... ``` fences if present
        if t.startswith("```"):
            # drop opening fence
            t = re.sub(r"^```[a-zA-Z0-9_]*", "", t).strip()
            # drop trailing fence
            if "```" in t:
                t = t.split("```", 1)[0].strip()
        
        return t


