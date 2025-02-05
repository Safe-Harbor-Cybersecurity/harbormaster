# src/harbormaster/core/config/settings.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    """
    Application settings and configuration.
    - API keys
    - Security parameters
    - Hugging Face integration settings
    """
    app_name: str = "Harbormaster"
    huggingface_token: str
    max_requests_per_minute: int = 100