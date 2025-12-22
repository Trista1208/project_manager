# src/core/base_llm.py
"""
Base LLM interface for multi-agent system.
All LLM clients must implement this interface.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LLMResponse:
    """Standardized response from any LLM."""
    content: str
    model: str
    provider: str
    tokens_used: int
    cost: float
    latency_ms: float
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class LLMMetrics:
    """Performance metrics for an LLM."""
    total_requests: int = 0
    total_tokens: int = 0
    total_cost: float = 0.0
    total_latency_ms: float = 0.0
    success_count: int = 0
    error_count: int = 0
    
    @property
    def avg_latency_ms(self) -> float:
        """Average latency per request."""
        if self.success_count == 0:
            return 0.0
        return self.total_latency_ms / self.success_count
    
    @property
    def success_rate(self) -> float:
        """Success rate as percentage."""
        total = self.success_count + self.error_count
        if total == 0:
            return 0.0
        return (self.success_count / total) * 100


class BaseLLM(ABC):
    """Abstract base class for all LLM implementations."""
    
    def __init__(self, api_key: str, model_name: str):
        """
        Initialize LLM client.
        
        Args:
            api_key: API key for the LLM provider
            model_name: Specific model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.metrics = LLMMetrics()
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters (temperature, max_tokens, etc.)
        
        Returns:
            LLMResponse with content and metadata
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Return the provider name (e.g., 'Google', 'OpenAI', 'DeepSeek')."""
        pass
    
    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for a request.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
        
        Returns:
            Estimated cost in USD
        """
        pass
    
    def update_metrics(self, response: LLMResponse, success: bool = True):
        """Update metrics after a request."""
        self.metrics.total_requests += 1
        
        if success:
            self.metrics.success_count += 1
            self.metrics.total_tokens += response.tokens_used
            self.metrics.total_cost += response.cost
            self.metrics.total_latency_ms += response.latency_ms
        else:
            self.metrics.error_count += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics as dictionary."""
        return {
            "provider": self.get_provider_name(),
            "model": self.model_name,
            "total_requests": self.metrics.total_requests,
            "success_count": self.metrics.success_count,
            "error_count": self.metrics.error_count,
            "success_rate": f"{self.metrics.success_rate:.2f}%",
            "total_tokens": self.metrics.total_tokens,
            "total_cost": f"${self.metrics.total_cost:.4f}",
            "avg_latency_ms": f"{self.metrics.avg_latency_ms:.2f}ms"
        }
    
    def reset_metrics(self):
        """Reset metrics to zero."""
        self.metrics = LLMMetrics()


