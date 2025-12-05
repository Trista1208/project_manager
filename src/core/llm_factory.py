# src/core/llm_factory.py
"""
Factory for creating LLM clients and multi-agent orchestrator.
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

from .base_llm import BaseLLM
from .llm_clients import GeminiClient, DeepSeekClient, OpenAIClient
from .multi_agent_orchestrator import MultiAgentOrchestrator, OrchestratorStrategy

# Load environment
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH)


class LLMFactory:
    """Factory for creating and configuring LLM clients."""
    
    @staticmethod
    def create_gemini_client(
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.0-flash-exp"
    ) -> Optional[GeminiClient]:
        """
        Create Gemini client.
        
        Args:
            api_key: API key (or from env)
            model_name: Model name
        
        Returns:
            GeminiClient or None if not configured
        """
        api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("⚠️  Gemini not configured: GOOGLE_API_KEY not set")
            return None
        
        try:
            return GeminiClient(api_key, model_name)
        except Exception as e:
            print(f"⚠️  Failed to create Gemini client: {e}")
            return None
    
    @staticmethod
    def create_deepseek_client(
        api_key: Optional[str] = None,
        model_name: str = "deepseek-reasoner"
    ) -> Optional[DeepSeekClient]:
        """
        Create DeepSeek R1 client.
        
        Args:
            api_key: API key (or from env)
            model_name: Model name
        
        Returns:
            DeepSeekClient or None if not configured
        """
        api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            print("⚠️  DeepSeek not configured: DEEPSEEK_API_KEY not set")
            return None
        
        try:
            return DeepSeekClient(api_key, model_name)
        except Exception as e:
            print(f"⚠️  Failed to create DeepSeek client: {e}")
            return None
    
    @staticmethod
    def create_openai_client(
        api_key: Optional[str] = None,
        model_name: str = "gpt-4o"
    ) -> Optional[OpenAIClient]:
        """
        Create OpenAI GPT client.
        
        Args:
            api_key: API key (or from env)
            model_name: Model name
        
        Returns:
            OpenAIClient or None if not configured
        """
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  OpenAI not configured: OPENAI_API_KEY not set")
            return None
        
        try:
            return OpenAIClient(api_key, model_name)
        except Exception as e:
            print(f"⚠️  Failed to create OpenAI client: {e}")
            return None
    
    @staticmethod
    def create_all_available_clients() -> List[BaseLLM]:
        """
        Create all available LLM clients based on environment configuration.
        
        Returns:
            List of configured LLM clients
        """
        clients = []
        
        # Try to create each client
        gemini = LLMFactory.create_gemini_client()
        if gemini:
            clients.append(gemini)
            print(f"✅ Gemini client configured: {gemini.model_name}")
        
        deepseek = LLMFactory.create_deepseek_client()
        if deepseek:
            clients.append(deepseek)
            print(f"✅ DeepSeek client configured: {deepseek.model_name}")
        
        openai = LLMFactory.create_openai_client()
        if openai:
            clients.append(openai)
            print(f"✅ OpenAI client configured: {openai.model_name}")
        
        if not clients:
            raise ValueError(
                "No LLM clients could be configured. "
                "Please set at least GOOGLE_API_KEY in .env"
            )
        
        return clients
    
    @staticmethod
    def create_orchestrator(
        strategy: Optional[str] = None,
        llm_clients: Optional[List[BaseLLM]] = None
    ) -> MultiAgentOrchestrator:
        """
        Create multi-agent orchestrator with configured strategy.
        
        Args:
            strategy: Strategy name (ensemble, specialized, fallback, single)
            llm_clients: List of LLM clients (or auto-create)
        
        Returns:
            MultiAgentOrchestrator instance
        """
        # Get or create LLM clients
        if llm_clients is None:
            llm_clients = LLMFactory.create_all_available_clients()
        
        # Parse strategy
        strategy_name = strategy or os.getenv("LLM_STRATEGY", "specialized")
        
        try:
            strategy_enum = OrchestratorStrategy[strategy_name.upper()]
        except KeyError:
            print(f"⚠️  Unknown strategy '{strategy_name}', using SPECIALIZED")
            strategy_enum = OrchestratorStrategy.SPECIALIZED
        
        orchestrator = MultiAgentOrchestrator(llm_clients, strategy_enum)
        
        print(f"🎯 Multi-agent orchestrator created:")
        print(f"   Strategy: {strategy_enum.value}")
        print(f"   LLMs: {len(llm_clients)} configured")
        
        return orchestrator

