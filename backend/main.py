"""
Blockchain Transaction Explainer - FastAPI Backend
Main application entry point with CORS middleware and route registration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routes import transaction, prediction, explanation
from services.model_loader import ModelLoader
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML models on startup"""
    print("🚀 Loading ML models...")
    ModelLoader.load_all_models()
    print("✅ All models loaded successfully!")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="Blockchain Transaction Explainer API",
    description="AI-powered blockchain transaction analysis and explanation",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(transaction.router, prefix="/api", tags=["Transaction"])
app.include_router(prediction.router, prefix="/api/predict", tags=["Predictions"])
app.include_router(explanation.router, prefix="/api", tags=["Explanation"])


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Blockchain Transaction Explainer",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models_loaded": ModelLoader.is_loaded(),
        "rpc_configured": bool(settings.RPC_URL)
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
