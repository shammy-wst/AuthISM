from pydantic import BaseModel, ConfigDict, Field
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class Settings(BaseModel):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AuthISM"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # Google Cloud Configuration
    GOOGLE_CLOUD_PROJECT: str = Field(default="authism-project")
    GOOGLE_CLOUD_BUCKET: str = Field(default="authism-storage")
    GOOGLE_APPLICATION_CREDENTIALS: str = Field(default="../credentials.json")
    
    # LLM Configuration
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    MODEL_NAME: str = Field(default="llama2")
    TEMPERATURE: float = Field(default=0.7)
    MAX_TOKENS: Optional[int] = Field(default=2000)
    CONTEXT_WINDOW: int = Field(default=4096)
    SYSTEM_PROMPT: str = Field(
        default="Tu es un assistant IA utile et honnête. "
        "Tu réponds toujours en français de manière claire et concise."
    )

    # MongoDB Configuration
    MONGODB_URL: str = Field(default="mongodb://localhost:27017")
    DATABASE_NAME: str = Field(default="authism")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()

# Debug print
print(f"Loaded settings:")
print(f"Project: {settings.GOOGLE_CLOUD_PROJECT}")
print(f"Bucket: {settings.GOOGLE_CLOUD_BUCKET}")
print(f"Credentials: {settings.GOOGLE_APPLICATION_CREDENTIALS}") 