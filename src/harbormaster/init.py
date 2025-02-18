# src/harbormaster/__init__.py
from typing import Dict, Any
from .core.config import Settings
from .security.scanners import PromptScanner
from .huggingface.adapters.model_adapter import ModelAdapter
from .huggingface.endpoints.inference import SecureInference

class HarborMaster:
    """
    Main class for Harbormaster functionality.
    Provides secure model management and inference.
    """
    def __init__(self, api_key: str):
        """Initialize Harbormaster with API key."""
        self.settings = Settings(api_key=api_key)
        self.model_adapter = ModelAdapter()
        self.secured_models: Dict[str, SecureInference] = {}
        
    async def secure_model(self, model_id: str) -> Dict[str, Any]:
        """
        Secure a Hugging Face model with Harbormaster protection.
        
        Args:
            model_id: The Hugging Face model ID to secure
            
        Returns:
            Dict containing security configuration and status
        """
        try:
            # Load and secure model
            model = await self.model_adapter.load_model(model_id)
            secure_model = SecureInference(model)
            
            # Cache secured model
            self.secured_models[model_id] = secure_model
            
            return {
                "status": "success",
                "message": f"Model {model_id} secured successfully",
                "config": {
                    "model_id": model_id,
                    "security_level": self.settings.security_level,
                    "rate_limit": self.settings.max_requests_per_minute,
                    "secured": True
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to secure model: {str(e)}"
            }

    async def predict(self, model_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a secure prediction using a secured model.
        
        Args:
            model_id: The secured model ID
            inputs: Model inputs
            
        Returns:
            Dict containing prediction results and security status
        """
        if model_id not in self.secured_models:
            return {
                "status": "error",
                "message": f"Model {model_id} not secured. Call secure_model() first."
            }
            
        return await self.secured_models[model_id].predict(inputs)

# Version info
__version__ = "1.0.0"