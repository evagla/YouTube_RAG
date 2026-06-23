"""
Define the LLM to use in rag_pipeline as well as query-expansion
For the fall-back option the Ollama model must be installed and will run on your local computer

"""

import requests
from config.config import load_settings


class OllamaClient:
    def __init__(self):
        # load centralized settings
        settings = load_settings()
        llm_config = settings.get("llm", {})

        # get settings from settings.yaml, and define fall-back values:
        self.model = llm_config.get("model", "llama3.2:latest")
        self.url = llm_config.get("api_url", "http://localhost:11434/api/chat")
        self.temperature = llm_config.get("temperature", 0.2)
        self.max_tokens = llm_config.get("max_tokens", 1024)

    def chat(self, messages, **kwargs):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        }
        # Ollama API uses 'num_predict' for max_tokens

        # add x-tra parameters if they occure
        payload.update(kwargs)

        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()


# A global client instance for run_rag to import:
client = OllamaClient()
