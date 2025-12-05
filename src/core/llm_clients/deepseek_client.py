# src/core/llm_clients/deepseek_client.py
"""
DeepSeek R1 LLM client implementation.
"""
import time
from datetime import datetime
from openai import OpenAI

from ..base_llm import BaseLLM, LLMResponse


class DeepSeekClient(BaseLLM):
    """DeepSeek R1 LLM client."""
    
    # Pricing per 1M tokens (DeepSeek R1)
    INPUT_PRICE_PER_1M = 0.55  # $0.55 per 1M input tokens
    OUTPUT_PRICE_PER_1M = 2.19  # $2.19 per 1M output tokens
    
    def __init__(self, api_key: str, model_name: str = "deepseek-reasoner"):
        """
        Initialize DeepSeek client.
        
        Args:
            api_key: DeepSeek API key
            model_name: DeepSeek model name (deepseek-reasoner for R1)
        """
        super().__init__(api_key, model_name)
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate response using DeepSeek R1.
        
        Args:
            prompt: Input prompt
            **kwargs: temperature, max_tokens, etc.
        
        Returns:
            LLMResponse object
        """
        start_time = time.time()
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 8000)  # R1 supports longer context
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract response data
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            # Calculate cost
            cost = self.estimate_cost(input_tokens, output_tokens)
            
            # DeepSeek R1 has reasoning tokens
            reasoning_content = getattr(response.choices[0].message, 'reasoning_content', None)
            
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
                    "reasoning_content": reasoning_content,
                    "finish_reason": response.choices[0].finish_reason
                }
            )
            
            self.update_metrics(llm_response, success=True)
            return llm_response
            
        except Exception as e:
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
    
    def get_provider_name(self) -> str:
        """Return provider name."""
        return "DeepSeek R1"
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for DeepSeek R1 request.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Cost in USD
        """
        input_cost = (input_tokens / 1_000_000) * self.INPUT_PRICE_PER_1M
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_PRICE_PER_1M
        return input_cost + output_cost


