"""
LLM Provider integrations for multiple AI services
"""

import os
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai


class LLMProvider(ABC):
    """Base class for LLM providers"""

    def __init__(self, model: str):
        self.model = model
        self.provider_name = self.__class__.__name__.replace("Provider", "")

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate response from LLM"""
        pass

    @abstractmethod
    def calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost based on token usage"""
        pass


class AnthropicProvider(LLMProvider):
    """Anthropic Claude provider"""

    # Pricing per 1M tokens (as of Dec 2024)
    PRICING = {
        "claude-opus-4-5": {"input": 15.00, "output": 75.00},
        "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
        "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},
        "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }

    def __init__(self, model: str):
        super().__init__(model)
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, max_tokens: int = 1024, **kwargs) -> Dict[str, Any]:
        """Generate response using Claude"""
        start_time = time.time()

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )

            latency = time.time() - start_time

            return {
                "output": response.content[0].text,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "latency": latency,
                "model": self.model,
                "provider": self.provider_name,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "output": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": time.time() - start_time,
                "model": self.model,
                "provider": self.provider_name,
                "success": False,
                "error": str(e)
            }

    def calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost based on token usage"""
        if not usage.get("success"):
            return 0.0

        pricing = self.PRICING.get(self.model, {"input": 3.00, "output": 15.00})
        input_cost = (usage["input_tokens"] / 1_000_000) * pricing["input"]
        output_cost = (usage["output_tokens"] / 1_000_000) * pricing["output"]
        return input_cost + output_cost


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""

    # Pricing per 1M tokens
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.150, "output": 0.600},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }

    def __init__(self, model: str):
        super().__init__(model)
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, max_tokens: int = 1024, **kwargs) -> Dict[str, Any]:
        """Generate response using GPT"""
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                **kwargs
            )

            latency = time.time() - start_time

            return {
                "output": response.choices[0].message.content,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "latency": latency,
                "model": self.model,
                "provider": self.provider_name,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "output": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": time.time() - start_time,
                "model": self.model,
                "provider": self.provider_name,
                "success": False,
                "error": str(e)
            }

    def calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost based on token usage"""
        if not usage.get("success"):
            return 0.0

        pricing = self.PRICING.get(self.model, {"input": 2.50, "output": 10.00})
        input_cost = (usage["input_tokens"] / 1_000_000) * pricing["input"]
        output_cost = (usage["output_tokens"] / 1_000_000) * pricing["output"]
        return input_cost + output_cost


class GoogleProvider(LLMProvider):
    """Google Gemini provider"""

    # Pricing per 1M tokens
    PRICING = {
        "gemini-2.0-flash-exp": {"input": 0.00, "output": 0.00},  # Free tier
        "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
        "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    }

    def __init__(self, model: str):
        super().__init__(model)
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def generate(self, prompt: str, max_tokens: int = 1024, **kwargs) -> Dict[str, Any]:
        """Generate response using Gemini"""
        start_time = time.time()

        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    **kwargs
                )
            )

            latency = time.time() - start_time

            # Gemini token counting
            input_tokens = self.client.count_tokens(prompt).total_tokens
            output_tokens = self.client.count_tokens(response.text).total_tokens

            return {
                "output": response.text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "latency": latency,
                "model": self.model,
                "provider": self.provider_name,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "output": None,
                "input_tokens": 0,
                "output_tokens": 0,
                "latency": time.time() - start_time,
                "model": self.model,
                "provider": self.provider_name,
                "success": False,
                "error": str(e)
            }

    def calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost based on token usage"""
        if not usage.get("success"):
            return 0.0

        pricing = self.PRICING.get(self.model, {"input": 1.25, "output": 5.00})
        input_cost = (usage["input_tokens"] / 1_000_000) * pricing["input"]
        output_cost = (usage["output_tokens"] / 1_000_000) * pricing["output"]
        return input_cost + output_cost


def get_provider(model: str) -> LLMProvider:
    """Factory function to get the appropriate provider for a model"""
    if "claude" in model.lower():
        return AnthropicProvider(model)
    elif "gpt" in model.lower():
        return OpenAIProvider(model)
    elif "gemini" in model.lower():
        return GoogleProvider(model)
    else:
        raise ValueError(f"Unknown model: {model}")
