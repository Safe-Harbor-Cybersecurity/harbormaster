# src/harbormaster/security/defenders/rate_limiter.py
from datetime import datetime, timedelta
from typing import Dict

class RateLimiter:
    """
    Rate limiting implementation for API protection.
    - Request tracking
    - Threshold enforcement
    - User-based limits
    """
    def __init__(self, window_seconds: int = 60, max_requests: int = 100):
        self.window_seconds = window_seconds
        self.max_requests = max_requests
        self.request_history: Dict[str, list] = {}

    def check_limit(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit.
        Returns True if request is allowed, False if limit exceeded.
        """
        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=self.window_seconds)

        # Initialize history for new users
        if user_id not in self.request_history:
            self.request_history[user_id] = []

        # Clean old requests
        self.request_history[user_id] = [
            timestamp for timestamp in self.request_history[user_id]
            if timestamp > window_start
        ]

        # Check limit
        if len(self.request_history[user_id]) >= self.max_requests:
            return False

        # Record new request
        self.request_history[user_id].append(current_time)
        return True

    def get_remaining_requests(self, user_id: str) -> int:
        """Get number of remaining requests allowed for user."""
        if user_id not in self.request_history:
            return self.max_requests

        current_time = datetime.utcnow()
        window_start = current_time - timedelta(seconds=self.window_seconds)
        
        recent_requests = len([
            timestamp for timestamp in self.request_history[user_id]
            if timestamp > window_start
        ])
        
        return max(0, self.max_requests - recent_requests)

    def reset_user(self, user_id: str) -> None:
        """Reset rate limit history for a user."""
        if user_id in self.request_history:
            del self.request_history[user_id]