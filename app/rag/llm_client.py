"""
Define the LLM to use in rag_pipeline
Here, the Ollama model must be installed and will run on your local computer

"""

import requests


class OllamaClient:
    def __init__(self, model: str = "llama3.2:latest"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def chat(self, messages):
        payload = {"model": self.model, "messages": messages, "stream": False}

        print("===PAYLOAD SENT TO OLLAMA ===")
        print(payload)
        print("=============================")

        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()


# A global client instance for run_rag to import:
client = OllamaClient()
