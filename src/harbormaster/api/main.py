# src/harbormaster/api/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from harbormaster.api.middleware.security import SecurityMiddleware
from harbormaster.api.routes import model_routes
from harbormaster.core.config.settings import Settings
import logging

# Initialize settings and logging
settings = Settings()
logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="API-based AI model security tool for Hugging Face models",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security middleware
app.add_middleware(SecurityMiddleware, settings=settings)

# Include routers
app.include_router(
    model_routes.router,
    prefix="/api/v1",
    tags=["models"]
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "environment": settings.env,
        "docs_url": "/docs",
        "health_check": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "harbormaster.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )