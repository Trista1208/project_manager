# src/core/llm_clients/groq_client.py
"""
Groq LLM client implementation (FREE alternative to OpenAI).
Groq provides free, ultra-fast inference with Llama and Mixtral models.
"""
import time
from datetime import datetime
from openai import OpenAI

from ..base_llm import BaseLLM, LLMResponse


class GroqClient(BaseLLM):
    """Groq LLM client - FREE and ultra-fast!"""
    
    # Pricing per 1M tokens (FREE tier available!)
    INPUT_PRICE_PER_1M = 0.00  # FREE!
    OUTPUT_PRICE_PER_1M = 0.00  # FREE!
    
    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key (get free at https://console.groq.com)
            model_name: Groq model name
                - llama-3.3-70b-versatile (recommended, fastest)
                - llama-3.1-70b-versatile
                - mixtral-8x7b-32768
                - gemma2-9b-it
        """
        super().__init__(api_key, model_name)
        
        # Groq uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
    
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate response using OpenAI GPT.
        
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
                max_tokens=kwargs.get("max_tokens", 4000)
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract response data
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            # Calculate cost
            cost = self.estimate_cost(input_tokens, output_tokens)
            
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
        return "Groq (FREE)"
    
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for Groq request.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Cost in USD (always 0.00 - FREE!)
        """
        return 0.00  # Groq is FREE!

