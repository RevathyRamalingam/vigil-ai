"""
Configuration settings for VigilAI Backend
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "VigilAI"
    DEBUG: bool = True
    APP_ENV: str = "development"
    
    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "vigilai"
    POSTGRES_USER: str = "vigilai"
    POSTGRES_PASSWORD: str = "vigilai123"
    SQLITE_URL: str = "sqlite:///./vigilai.db"
    USE_SQLITE: bool = True
    
    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return self.SQLITE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    # MinIO (S3-compatible storage)
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "vigilai-uploads"
    MINIO_SECURE: bool = False
    
    # ML Model
    MODEL_PATH: str = "models/yolov8n.pt"
    CONFIDENCE_THRESHOLD: float = 0.6
    FRAME_EXTRACTION_FPS: int = 1
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 500 * 1024 * 1024  # 500MB
    ALLOWED_VIDEO_EXTENSIONS: List[str] = [".mp4", ".avi", ".mov", ".mkv"]
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png"]
    
    # Processing
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()