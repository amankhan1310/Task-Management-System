import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Task Management System"
    APP_ENV: str = "development"
    
    # Database Settings
    # This creates tasks.db in your project root
    SQLITE_PATH: str = "tasks.db" 
    
    # Auth Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-me")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # Kafka Settings
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_SERVERS", "localhost:9092")
    KAFKA_TOPIC: str = "task-events"

    class Config:
        case_sensitive = True

settings = Settings()