import yaml
import os
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
from config import get_settings

logger = logging.getLogger(__name__)

class BaseAgent:
    """
    Base class for all specialist agents. 
    Loads configuration from YAML and provides standard LLM interaction.
    """
    def __init__(self, config_path: str):
        self.settings = get_settings()
        self.config = self._load_config(config_path)
        self.name = self.config.get("name", "base_agent")
        logger.info(f"Initialized agent: {self.name} with config from {config_path}")
        
        # Initialize NIM client
        self.client = OpenAI(
            base_url=self.settings.nim_base_url,
            api_key=os.getenv("NVIDIA_API_KEY") or self.settings.nvidia_api_key
        )
        self.model = self.config.get("llm", {}).get("model", self.settings.primary_model)
        self.temperature = self.config.get("llm", {}).get("temperature", 0.1)

    def _load_config(self, path: str) -> Dict:
        if not os.path.exists(path):
            logger.error(f"Config file not found: {path}")
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f)

    async def run(self, user_input: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        To be implemented by specialized agents.
        """
        raise NotImplementedError("Subclasses must implement run()")

    def get_system_prompt(self) -> str:
        return self.config.get("system_prompt", "You are a helpful assistant.")

    @staticmethod
    def extract_content(response) -> Optional[str]:
        """
        Extracts text content from a NIM response, checking both
        standard 'content' and Nemotron-specific 'reasoning_content'.
        """
        msg = response.choices[0].message
        content = msg.content
        if content is None:
            content = getattr(msg, "reasoning_content", None)
            if content is None and hasattr(msg, "model_extra"):
                content = msg.model_extra.get("reasoning_content")
        return str(content) if content else None
