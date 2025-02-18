# src/harbormaster/api/middleware/security.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import logging
from typing import Optional
from datetime import datetime

from harbormaster.core.config.settings import Settings
from harbormaster.security.defenders.rate_limiter import RateLimiter

class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling security aspects of API requests.
    - Token validation
    - Rate limiting 
    - Request logging
    """
    def __init__(self, app, settings: Optional[Settings] = None):
        super().__init__(app)
        self.settings = settings or Settings()
        self.rate_limiter = RateLimiter()
        self.logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            # Token validation
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Missing authentication token")
            
            if not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid token format")
            
            # Rate limiting check
            client_ip = request.client.host
            if not self.rate_limiter.check_limit(client_ip):
                raise HTTPException(status_code=429, detail="Rate limit exceeded")

            # Request logging
            self.logger.info(
                f"Request: {request.method} {request.url} "
                f"Client: {client_ip} "
                f"Time: {datetime.utcnow().isoformat()}"
            )

            # Continue with the request
            response = await call_next(request)
            
            # Add security headers
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            
            return response

        except HTTPException as e:
            self.logger.warning(f"Security check failed: {str(e)}")
            raise e
        except Exception as e:
            self.logger.error(f"Security middleware error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal security error")
