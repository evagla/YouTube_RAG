import os
from pathlib import Path
import yaml
from dotenv import load_dotenv


# 1. Define the project root path automatically using pathlib.
# __file__ points to this file (config/config.py).
# .parent.parent moves two levels up to the YouTube_RAG directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.yaml"


def load_settings() -> dict:
    """
    Loads configuration from settings.yaml and injects secrets from .env.

    Returns:
        dict: A dictionary containing all application configuration and secrets.
    """

    # Load the local .env file if it exists
    load_dotenv(PROJECT_ROOT / ".env")

    # Verify that settings.yaml actually exists
    if not CONFIG_PATH.exists():
        print("if")
        raise FileNotFoundError(
            f"Configuration file not found at: {CONFIG_PATH}. "
            f"Please copy settings.yaml.example to settings.yaml first!"
        )

    # Read and parse the YAML file into a Python dictionary
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        # safe_load is a security best practice to prevent arbitrary code execution
        settings = yaml.safe_load(f)

    # 2. Inject sensitive credentials from environment variables (.env)
    # This keeps secrets out of the public version-controlled YAML files.
    if "database" in settings:
        settings["database"]["user"] = os.getenv("DATABASE_USER", "")
        settings["database"]["password"] = os.getenv("DATABASE_PASSWORD", "")

    # Gather API keys into a dedicated section for easy access, if using...
    settings["api_keys"] = {
        "openai": os.getenv("OPENAI_API_KEY", ""),
        "huggingface": os.getenv("HUGGINGFACE_TOKEN", ""),
    }

    return settings
