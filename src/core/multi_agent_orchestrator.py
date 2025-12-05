# src/core/multi_agent_orchestrator.py
"""
Multi-Agent LLM Orchestrator with multiple strategies.
Coordinates multiple LLMs for better results.
"""
import json
from typing import List, Dict, Any, Optional
from enum import Enum

from .base_llm import BaseLLM, LLMResponse


class OrchestratorStrategy(Enum):
    """Available orchestration strategies."""
    ENSEMBLE = "ensemble"  # All LLMs vote, pick best/consensus
    SPECIALIZED = "specialized"  # Each LLM handles specific tasks
    FALLBACK = "fallback"  # Try cheap first, fallback to expensive
    SINGLE = "single"  # Use only one LLM (default behavior)


class MultiAgentOrchestrator:
    """Orchestrates multiple LLMs for task breakdown."""
    
    def __init__(
        self,
        llm_clients: List[BaseLLM],
        strategy: OrchestratorStrategy = OrchestratorStrategy.SPECIALIZED
    ):
        """
        Initialize multi-agent orchestrator.
        
        Args:
            llm_clients: List of LLM clients to orchestrate
            strategy: Orchestration strategy to use
        """
        self.llm_clients = llm_clients
        self.strategy = strategy
        
        if not llm_clients:
            raise ValueError("At least one LLM client must be provided")
    
    def generate(
        self, 
        prompt: str, 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response using configured strategy.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
        
        Returns:
            Dictionary with result and metadata
        """
        if self.strategy == OrchestratorStrategy.ENSEMBLE:
            return self._ensemble_strategy(prompt, **kwargs)
        elif self.strategy == OrchestratorStrategy.SPECIALIZED:
            return self._specialized_strategy(prompt, **kwargs)
        elif self.strategy == OrchestratorStrategy.FALLBACK:
            return self._fallback_strategy(prompt, **kwargs)
        else:  # SINGLE
            return self._single_strategy(prompt, **kwargs)
    
    def _single_strategy(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Use only the first LLM (simplest strategy).
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
        
        Returns:
            Result dictionary
        """
        llm = self.llm_clients[0]
        
        try:
            response = llm.generate(prompt, **kwargs)
            
            return {
                "success": True,
                "content": response.content,
                "strategy": "single",
                "provider_used": response.provider,
                "model_used": response.model,
                "cost": response.cost,
                "latency_ms": response.latency_ms,
                "tokens_used": response.tokens_used,
                "metadata": {
                    "response": response
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "strategy": "single",
                "provider_used": llm.get_provider_name()
            }
    
    def _ensemble_strategy(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Query all LLMs and pick the best response.
        Criteria: Longest valid JSON, or consensus if multiple valid.
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
        
        Returns:
            Result dictionary with all responses and best selection
        """
        responses = []
        total_cost = 0.0
        total_latency = 0.0
        
        # Query all LLMs
        for llm in self.llm_clients:
            try:
                response = llm.generate(prompt, **kwargs)
                responses.append({
                    "provider": response.provider,
                    "model": response.model,
                    "content": response.content,
                    "cost": response.cost,
                    "latency_ms": response.latency_ms,
                    "tokens": response.tokens_used,
                    "success": True,
                    "response_obj": response
                })
                total_cost += response.cost
                total_latency += response.latency_ms
            except Exception as e:
                responses.append({
                    "provider": llm.get_provider_name(),
                    "model": llm.model_name,
                    "error": str(e),
                    "success": False
                })
        
        # Select best response
        successful_responses = [r for r in responses if r.get("success")]
        
        if not successful_responses:
            return {
                "success": False,
                "error": "All LLMs failed",
                "strategy": "ensemble",
                "responses": responses
            }
        
        # Pick best response (longest valid JSON or most tokens)
        best_response = max(
            successful_responses,
            key=lambda r: len(r["content"]) if self._is_valid_json(r["content"]) else 0
        )
        
        return {
            "success": True,
            "content": best_response["content"],
            "strategy": "ensemble",
            "provider_used": best_response["provider"],
            "model_used": best_response["model"],
            "cost": total_cost,
            "latency_ms": total_latency,
            "tokens_used": sum(r.get("tokens", 0) for r in successful_responses),
            "metadata": {
                "all_responses": responses,
                "successful_count": len(successful_responses),
                "failed_count": len(responses) - len(successful_responses),
                "selected_provider": best_response["provider"]
            }
        }
    
    def _specialized_strategy(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Use specialized LLMs for different tasks.
        - Gemini: Fast task breakdown (default)
        - DeepSeek R1: Complex reasoning and validation
        - GPT-4: Planning and optimization
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
        
        Returns:
            Result dictionary
        """
        task_type = kwargs.get("task_type", "breakdown")
        
        # Select LLM based on task type
        if task_type == "validation" and len(self.llm_clients) > 1:
            # Use DeepSeek R1 for validation
            selected_llm = next(
                (llm for llm in self.llm_clients if "deepseek" in llm.model_name.lower()),
                self.llm_clients[1] if len(self.llm_clients) > 1 else self.llm_clients[0]
            )
        elif task_type == "planning" and len(self.llm_clients) > 2:
            # Use GPT-4 for planning
            selected_llm = next(
                (llm for llm in self.llm_clients if "gpt" in llm.model_name.lower()),
                self.llm_clients[2] if len(self.llm_clients) > 2 else self.llm_clients[0]
            )
        else:
            # Use Gemini for fast breakdown (default)
            selected_llm = next(
                (llm for llm in self.llm_clients if "gemini" in llm.model_name.lower()),
                self.llm_clients[0]
            )
        
        try:
            response = selected_llm.generate(prompt, **kwargs)
            
            return {
                "success": True,
                "content": response.content,
                "strategy": "specialized",
                "task_type": task_type,
                "provider_used": response.provider,
                "model_used": response.model,
                "cost": response.cost,
                "latency_ms": response.latency_ms,
                "tokens_used": response.tokens_used,
                "metadata": {
                    "selection_reason": f"Selected {response.provider} for {task_type}",
                    "response": response
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "strategy": "specialized",
                "task_type": task_type,
                "provider_used": selected_llm.get_provider_name()
            }
    
    def _fallback_strategy(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Try LLMs in order (cheap to expensive), stop on first success.
        Order: Gemini → DeepSeek → GPT-4
        
        Args:
            prompt: Input prompt
            **kwargs: Additional parameters
        
        Returns:
            Result dictionary
        """
        # Sort LLMs by cost (cheapest first)
        sorted_llms = sorted(
            self.llm_clients,
            key=lambda llm: llm.estimate_cost(1000, 1000)  # Estimate for 1k tokens
        )
        
        attempts = []
        
        for llm in sorted_llms:
            try:
                response = llm.generate(prompt, **kwargs)
                
                # Validate response is usable
                if response.content and len(response.content) > 10:
                    return {
                        "success": True,
                        "content": response.content,
                        "strategy": "fallback",
                        "provider_used": response.provider,
                        "model_used": response.model,
                        "cost": response.cost,
                        "latency_ms": response.latency_ms,
                        "tokens_used": response.tokens_used,
                        "metadata": {
                            "attempts": attempts + [{
                                "provider": response.provider,
                                "success": True
                            }],
                            "fallback_level": len(attempts),
                            "response": response
                        }
                    }
            except Exception as e:
                attempts.append({
                    "provider": llm.get_provider_name(),
                    "error": str(e),
                    "success": False
                })
        
        return {
            "success": False,
            "error": "All LLMs failed in fallback chain",
            "strategy": "fallback",
            "metadata": {
                "attempts": attempts
            }
        }
    
    def get_all_metrics(self) -> List[Dict[str, Any]]:
        """Get metrics from all LLM clients."""
        return [llm.get_metrics() for llm in self.llm_clients]
    
    def reset_all_metrics(self):
        """Reset metrics for all LLM clients."""
        for llm in self.llm_clients:
            llm.reset_metrics()
    
    @staticmethod
    def _is_valid_json(content: str) -> bool:
        """Check if content is valid JSON."""
        try:
            json.loads(content)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

