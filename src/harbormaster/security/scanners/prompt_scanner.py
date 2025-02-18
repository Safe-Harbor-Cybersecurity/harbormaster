# src/harbormaster/security/scanners/prompt_scanner.py
from typing import Dict, Any
import re
import json

class PromptScanner:
    """
    Scanner for detecting and preventing prompt injection attacks.
    - Pattern matching
    - Semantic analysis
    - Risk scoring
    """
    def __init__(self):
        # Common injection patterns
        self.patterns = {
            "system_command": r"(?i)(system|exec|eval|os\.|subprocess)",
            "sql_injection": r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP|UNION)",
            "path_traversal": r"\.{2}[/\\]",
            "control_chars": r"[\x00-\x1F\x7F]",
            "model_prompt": r"(?i)(you are|ignore|forget|don't|do not)"
        }
        
        # Risk scoring weights
        self.weights = {
            "system_command": 1.0,
            "sql_injection": 0.8,
            "path_traversal": 0.9,
            "control_chars": 0.7,
            "model_prompt": 0.6
        }

    def scan(self, prompt: str) -> Dict[str, Any]:
        """
        Scans input prompt for potential security risks.
        Returns dict with risk assessment and details.
        """
        matches = {}
        total_risk = 0.0
        
        # Check each pattern
        for name, pattern in self.patterns.items():
            found = re.findall(pattern, prompt)
            if found:
                matches[name] = found
                total_risk += self.weights[name] * len(found)
                
        # Calculate risk level
        risk_level = self._calculate_risk_level(total_risk)
        
        # Build scan result
        result = {
            "risk_level": risk_level,
            "risk_score": round(total_risk, 2),
            "matches": matches,
            "input_length": len(prompt),
            "reason": self._get_risk_reason(matches) if matches else "No risks detected",
            "timestamp": self._get_timestamp()
        }
        
        return result

    def _calculate_risk_level(self, risk_score: float) -> str:
        """Determines risk level based on score."""
        if risk_score >= 1.0:
            return "high"
        elif risk_score >= 0.5:
            return "medium"
        return "low"

    def _get_risk_reason(self, matches: Dict) -> str:
        """Generates explanation of detected risks."""
        reasons = []
        for pattern_name, found in matches.items():
            reasons.append(f"Found {pattern_name} pattern: {json.dumps(found)}")
        return "; ".join(reasons)

    def _get_timestamp(self) -> str:
        """Returns current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()