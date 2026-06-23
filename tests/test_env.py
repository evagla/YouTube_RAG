import os
from config.config import load_settings

settings = load_settings()

print("DB user:", settings["database"].get("user"))
print("DB password:", settings["database"].get("password"))
print("OpenAI key:", settings["api_keys"].get("openai"))
print("HF token:", settings["api_keys"].get("huggingface"))
