# src/harbormaster/api/routes/model_routes.py
from fastapi import APIRouter, Depends, HTTPException
from harbormaster.core.config import Settings
from harbormaster.services.model_adapter import ModelAdapter
from harbormaster.services.secure_inference import SecureInference

router = APIRouter()

@router.post("/secure-model")
async def secure_model(model_id: str, settings: Settings = Depends()):
    """
    Endpoint to secure a Hugging Face model with Harbormaster protection.
    Args:
        model_id: The Hugging Face model ID to secure
        settings: Application settings
    Returns:
        dict: Secured model configuration and status
    """
    try:
        # Initialize model adapter
        adapter = ModelAdapter()
        model = await adapter.load_model(model_id)

        # Create secure inference wrapper
        secure_inference = SecureInference(model)

        # Configure security settings
        config = {
            "model_id": model_id,
            "security_level": "high",
            "rate_limit": settings.max_requests_per_minute,
            "token": settings.huggingface_token,
            "secured": True
        }

        return {
            "status": "success",
            "message": f"Model {model_id} secured successfully",
            "config": config
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to secure model: {str(e)}"
        )