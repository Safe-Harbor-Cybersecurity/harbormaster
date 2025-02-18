# src/harbormaster/core/config/settings.py
from pydantic import BaseSettings, Field, SecretStr

class Settings(BaseSettings):
    """
    Application settings and configuration.
    - API keys
    - Security parameters
    - Hugging Face integration settings
    """
    # Application settings
    app_name: str = "Harbormaster"
    env: str = Field(default="development", env="HARBORMASTER_ENV")
    debug: bool = Field(default=False, env="HARBORMASTER_DEBUG")

    # Security settings
    huggingface_token: SecretStr = Field(..., env="HUGGINGFACE_TOKEN")
    api_key: SecretStr = Field(..., env="HARBORMASTER_API_KEY")
    max_requests_per_minute: int = Field(default=100, env="MAX_REQUESTS_PER_MINUTE")
    security_level: str = Field(default="high", env="SECURITY_LEVEL")

    # Model settings
    model_cache_dir: str = Field(default="./model_cache", env="MODEL_CACHE_DIR")
    default_model: str = Field(default="bert-base-uncased", env="DEFAULT_MODEL")

    # Logging settings
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    enable_audit_logging: bool = Field(default=True, env="ENABLE_AUDIT_LOGGING")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False