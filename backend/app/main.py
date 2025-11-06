"""
Main FastAPI application
"""

from fastapi import FastAPI
from app.routers import evaluator_routers

# Create FastAPI app
app = FastAPI(
    title="AI Privacy Evaluator API",
    description="API para avaliar políticas de privacidade usando IA",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Include routers
app.include_router(evaluator_routers.router)


# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint to verify the API is running
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "message": "AI Privacy Evaluator API is running"
    }



