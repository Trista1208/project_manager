# src/core/llm.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env from project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(ENV_PATH)

class LLMClient:
    def __init__(self):
        # Try GitHub Models first (FREE! You already have the token!)
        github_token = os.getenv("GITHUB_TOKEN")
        gemini_key = os.getenv("GOOGLE_API_KEY")
        
        if github_token:
            # Use GitHub Models (FREE!)
            self.client = OpenAI(
                api_key=github_token,
                base_url="https://models.inference.ai.azure.com"
            )
            self.model = "gpt-4o-mini"
            self.provider = "GitHub Models (FREE!)"
        elif gemini_key:
            # Fallback to Gemini
            self.client = OpenAI(
                api_key=gemini_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
            self.model = "gemini-2.0-flash-exp"
            self.provider = "Google Gemini"
        else:
            raise ValueError(
                "No LLM API key configured!\n"
                "You have two FREE options:\n"
                "1. Use GitHub Models (you already have GITHUB_TOKEN!)\n"
                "   - Set GITHUB_TOKEN in .env (you already have it!)\n"
                "2. Use Gemini (get FREE key)\n"
                "   - Get key: https://aistudio.google.com/app/apikey\n"
                "   - Set GOOGLE_API_KEY in .env"
            )

    def run(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
