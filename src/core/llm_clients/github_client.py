# src/core/llm_clients/github_client.py
"""
GitHub Models LLM client.
Uses GitHub Models API (FREE!) - requires GitHub token.
"""
import os
import time
from datetime import datetime
from openai import OpenAI
from ..base_llm import BaseLLM, LLMResponse


class GitHubClient(BaseLLM):
    """GitHub Models client using OpenAI-compatible API."""
    
    # Pricing (FREE!)
    INPUT_PRICE_PER_1M = 0.0
    OUTPUT_PRICE_PER_1M = 0.0
    
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
        
        super().__init__(github_token, model_name)
        
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
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate response using GitHub Models.
        
        Args:
            prompt: Input prompt
            **kwargs: temperature, max_tokens, etc.
        
        Returns:
            LLMResponse object
        """
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2000)
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract response data
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if hasattr(response, 'usage') else 0
            input_tokens = response.usage.prompt_tokens if hasattr(response, 'usage') else 0
            output_tokens = response.usage.completion_tokens if hasattr(response, 'usage') else 0
            
            # Cost is always 0 for GitHub Models
            cost = 0.0
            
            llm_response = LLMResponse(
                content=content,
                model=self.model_name,
                provider=self.get_provider_name(),
                tokens_used=tokens_used,
                cost=cost,
                latency_ms=latency_ms,
                timestamp=datetime.now().isoformat(),
                metadata={
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "finish_reason": response.choices[0].finish_reason if hasattr(response.choices[0], 'finish_reason') else "unknown"
                }
            )
            
            self.update_metrics(llm_response, success=True)
            return llm_response
            
        except Exception as e:
            # Return error response
            latency_ms = (time.time() - start_time) * 1000
            error_response = LLMResponse(
                content=f"Error: {str(e)}",
                model=self.model_name,
                provider=self.get_provider_name(),
                tokens_used=0,
                cost=0.0,
                latency_ms=latency_ms,
                timestamp=datetime.now().isoformat(),
                metadata={"error": str(e)}
            )
            self.update_metrics(error_response, success=False)
            raise
    
    def run(self, prompt: str) -> str:
        """
        Run inference using GitHub Models (backward compatibility).
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            The model's response as a string
        """
        response = self.generate(prompt)
        return response.content
    
    def get_provider_name(self) -> str:
        """Return provider name."""
        return "GitHub Models"
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
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
    
    def get_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Alias for estimate_cost (backward compatibility)."""
        return self.estimate_cost(input_tokens, output_tokens)

