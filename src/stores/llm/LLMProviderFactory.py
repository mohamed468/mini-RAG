from .LLMEnums import LLEnums
from .providers import OpenAIProvider, CoHereProvider, GeminiProvider
from helpers.config import Settings
from typing import Optional

class LLMProviderFactory:
    def __init__(self, config: Settings):
        self.config = config
    
    def _validate_api_key(self, key: Optional[str], provider_name: str) -> str:
        """التحقق من وجود المفتاح"""
        if not key:
            raise ValueError(f"{provider_name}_API_KEY is not set in environment variables.")
        return key
    
    def create(self, provider: str):
        if provider == LLEnums.OPENAI.value:
            api_key = self._validate_api_key(self.config.OPENAI_API_KEY, "OPENAI")
            return OpenAIProvider(
                api_key=api_key,
                api_url=self.config.OPENAI_API_URL or "",
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS or 1000,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS or 1000,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE or 0.1
            )
        
        if provider == LLEnums.COHERE.value:
            api_key = self._validate_api_key(self.config.COHERE_API_KEY, "COHERE")
            return CoHereProvider(
                api_key=api_key,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS or 1000,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS or 1000,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE or 0.1
            )
        
        if provider == LLEnums.GEMINI.value:
            api_key = self._validate_api_key(self.config.GEMINI_API_KEY, "GEMINI")
            return GeminiProvider(
                api_key=api_key,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS or 1000,
                default_generation_max_output_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS or 1000,
                default_generation_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE or 0.1
            )
        
        raise ValueError(f"Unknown provider: {provider}")