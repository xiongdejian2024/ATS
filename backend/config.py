"""应用配置"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import json


class Settings(BaseSettings):
    """应用配置类"""
    
    # 项目信息
    PROJECT_NAME: str = "ATS-Backend"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://ats_user:ats_password@localhost:3306/ats_db"
    DATABASE_POOL_SIZE: int = Field(default=10, ge=1, le=100)
    DATABASE_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    DATABASE_POOL_TIMEOUT: int = Field(default=30, ge=1, le=300)
    DATABASE_CONNECT_TIMEOUT: int = Field(default=10, ge=1, le=120)
    DATABASE_SCHEMA: str = Field(default="", pattern=r"^(?:[a-z][a-z0-9_]{0,62})?$")
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # RabbitMQ配置
    RABBITMQ_URL: str = "amqp://ats_user:ats_password@localhost:5672"
    
    # JWT配置
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-change-in-production"
    # 可独立配置；为空时使用持久 JWT 密钥派生 AI 配置加密密钥。
    AI_ENCRYPTION_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    
    # MinIO配置
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = "ats-files"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/ats.log"
    
    # 环境
    ENVIRONMENT: str = "development"
    ATS_REQUIRE_ORIGIN_AUTH: bool = False
    ATS_ORIGIN_SERVICE_KEY: str = ""
    TASK_SCHEDULER_ENABLED: bool = True
    
    # 文件上传配置
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".png", ".jpg", ".jpeg", ".gif",
        ".txt", ".log", ".csv", ".xmind", ".zip"
    ]
    
    # Celery配置
    CELERY_BROKER_URL: str = "amqp://ats_user:ats_password@localhost:5672"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # WebSocket配置
    WEBSOCKET_HOST: str = "localhost"
    WEBSOCKET_PORT: int = 8000
    WEBSOCKET_PATH: str = "/ws/agent"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> any:
            if field_name == "BACKEND_CORS_ORIGINS":
                if isinstance(raw_val, str):
                    try:
                        return json.loads(raw_val)
                    except json.JSONDecodeError:
                        return [origin.strip() for origin in raw_val.split(",")]
            return cls.json_loads(raw_val)


settings = Settings()
