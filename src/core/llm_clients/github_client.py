# src/core/llm_clients/github_client.py
"""
GitHub Models LLM client.
Uses GitHub Models API (FREE!) - requires GitHub token.
"""
import os
from openai import OpenAI
from src.core.base_llm import BaseLLM


class GitHubClient(BaseLLM):
    """GitHub Models client using OpenAI-compatible API."""
    
    def __init__(self, api_key: str = None, model_name: str = "gpt-4o-mini"):
        """
        Initialize GitHub Models client.
        
        Args:
            api_key: GitHub token (optional, will try environment if not provided)
            model_name: Model to use (default: gpt-4o-mini)
        """
        github_token = api_key or os.getenv("GITHUB_TOKEN")
        
        if not github_token:
            raise ValueError("GITHUB_TOKEN not found in environment")
        
        self.client = OpenAI(
            api_key=github_token,
            base_url="https://models.inference.ai.azure.com"
        )
        
        # Use specified model (defaults to GPT-4o-mini - FREE and very capable!)
        self.model = model_name
        self.provider = "GitHub Models"
        
        # Pricing (FREE!)
        self.input_cost_per_million = 0.0
        self.output_cost_per_million = 0.0
    
    def run(self, prompt: str) -> str:
        """
        Run inference using GitHub Models.
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            The model's response as a string
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost for token usage.
        
        GitHub Models is FREE!
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost (always 0.0 for GitHub Models)
        """
        return 0.0

