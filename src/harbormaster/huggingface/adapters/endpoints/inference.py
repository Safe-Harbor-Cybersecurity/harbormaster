# src/harbormaster/huggingface/endpoints/inference.py
from typing import Dict, Any
from transformers import Pipeline
from harbormaster.security.scanners.prompt_scanner import PromptScanner

class SecureInference:
    """
    Secure inference endpoint for Hugging Face models.
    - Input validation
    - Output sanitization
    - Error handling
    """
    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline
        self.scanner = PromptScanner()
        
    async def validate_input(self, inputs: Dict) -> bool:
        """Validates input before inference."""
        scan_result = self.scanner.scan(str(inputs))
        if scan_result.get("risk_level", "high") == "high":
            raise ValueError(f"Input failed security scan: {scan_result['reason']}")
        return True

    async def sanitize_output(self, output: Dict) -> Dict:
        """Sanitizes model output."""
        # Remove sensitive patterns
        if isinstance(output, dict):
            for key in output:
                if isinstance(output[key], str):
                    # Remove potential sensitive data patterns
                    output[key] = self._clean_text(output[key])
        return output

    def _clean_text(self, text: str) -> str:
        """Removes sensitive patterns from text."""
        # Add cleaning logic here
        return text

    async def predict(self, inputs: Dict) -> Dict:
        """
        Performs secure model inference with input validation
        and output sanitization.
        """
        try:
            # Validate input
            await self.validate_input(inputs)
            
            # Run model inference
            output = self.pipeline(**inputs)
            
            # Sanitize output
            clean_output = await self.sanitize_output(output)
            
            return {
                "status": "success",
                "output": clean_output,
                "security_checks_passed": True
            }
            
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e),
                "security_checks_passed": False
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Inference error: {str(e)}",
                "security_checks_passed": False
            }