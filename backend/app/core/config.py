import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TFT Strategy Advisor"
    OPENAI_API_KEY: str
    CURRENT_PATCH: str = "14.3"
    CHROMA_DB_DIR: str = "/app/data/chroma_db"
    
    class Config:
        env_file = ".env"

settings = Settings()
