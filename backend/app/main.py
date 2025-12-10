"""
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import evaluator_routers
from app.utils.logger import SetupLogger

# Initialize logger
SetupLogger.setup_logger()
print("=" * 50)
print("AI Privacy Evaluator API - Logger Initialized")
print("=" * 50)

# Create FastAPI app
app = FastAPI(
    title="AI Privacy Evaluator API",
    description="API para avaliar políticas de privacidade usando IA",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "chrome-extension://*",
        "moz-extension://*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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



