# src/harbormaster/services/model_adapter.py
from transformers import AutoModel, AutoTokenizer, Pipeline
from typing import Dict, Any, Optional
from huggingface_hub import HfApi
import logging

from harbormaster.core.config.settings import Settings
from harbormaster.huggingface.endpoints.inference import SecureInference

class ModelAdapter:
    """
    Service for managing model loading and configuration.
    Provides security-focused model initialization.
    """
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.api = HfApi(token=self.settings.huggingface_token.get_secret_value())
        self.logger = logging.getLogger(__name__)
        self.model_cache: Dict[str, Pipeline] = {}

    async def load_model(self, model_id: str) -> Pipeline:
        """
        Loads a Hugging Face model with security checks.
        
        Args:
            model_id: The Hugging Face model ID to load
            
        Returns:
            Pipeline: Configured model pipeline
        """
        try:
            # Check cache first
            if model_id in self.model_cache:
                self.logger.info(f"Loading {model_id} from cache")
                return self.model_cache[model_id]

            # Validate model
            if not await self.validate_model(model_id):
                raise ValueError(f"Model {model_id} validation failed")

            # Load model components
            self.logger.info(f"Loading model: {model_id}")
            model = await self._load_model_safely(model_id)
            tokenizer = await self._load_tokenizer_safely(model_id)

            # Create pipeline
            pipeline = Pipeline(
                model=model,
                tokenizer=tokenizer,
                task=await self._detect_task(model_id)
            )

            # Cache pipeline
            self.model_cache[model_id] = pipeline
            return pipeline

        except Exception as e:
            self.logger.error(f"Error loading model {model_id}: {str(e)}")
            raise

    async def validate_model(self, model_id: str) -> bool:
        """Validates model before loading."""
        try:
            model_info = self.api.model_info(model_id)
            return bool(model_info) and model_info.tags is not None
        except Exception as e:
            self.logger.error(f"Model validation failed: {str(e)}")
            return False

    async def _load_model_safely(self, model_id: str) -> AutoModel:
        """Safely loads model with error handling."""
        try:
            return AutoModel.from_pretrained(
                model_id,
                cache_dir=self.settings.model_cache_dir,
                trust_remote_code=False
            )
        except Exception as e:
            self.logger.error(f"Model loading failed: {str(e)}")
            raise

    async def _load_tokenizer_safely(self, model_id: str) -> AutoTokenizer:
        """Safely loads tokenizer with error handling."""
        try:
            return AutoTokenizer.from_pretrained(
                model_id,
                cache_dir=self.settings.model_cache_dir,
                trust_remote_code=False
            )
        except Exception as e:
            self.logger.error(f"Tokenizer loading failed: {str(e)}")
            raise

    async def _detect_task(self, model_id: str) -> str:
        """Detects appropriate task for model."""
        try:
            model_info = self.api.model_info(model_id)
            return model_info.pipeline_tag or "text-classification"
        except:
            return "text-classification"