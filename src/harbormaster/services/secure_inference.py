# src/harbormaster/services/secure_inference.py
from typing import Dict, Any
from transformers import Pipeline
from harbormaster.security.scanners.prompt_scanner import PromptScanner

class SecureInference:
    def __init__(self, model: Pipeline):
        self.model = model
        self.scanner = PromptScanner()

    async def predict(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate input
            scan_result = self.scanner.scan(str(inputs))
            if scan_result["risk_level"] == "high":
                return {
                    "status": "error",
                    "message": f"Security check failed: {scan_result['reason']}",
                    "security_checks_passed": False
                }

            # Make prediction
            output = self.model(**inputs)

            return {
                "status": "success",
                "output": output,
                "security_checks_passed": True
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "security_checks_passed": False
            }