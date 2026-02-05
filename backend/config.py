"""
Configuration settings for the backend application
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # RPC Configuration
    RPC_URL: str = os.getenv("RPC_URL", "https://eth-mainnet.g.alchemy.com/v2/demo")
    ALCHEMY_API_KEY: str = os.getenv("ALCHEMY_API_KEY", "")
    INFURA_API_KEY: str = os.getenv("INFURA_API_KEY", "")
    
    # Model paths
    MODELS_DIR: str = os.getenv("MODELS_DIR", "../")
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Cache settings
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    CACHE_TTL: int = 3600  # 1 hour
    
    # API rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
