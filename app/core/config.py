from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Travel Intelligence System"
    API_V1_STR: str = "/api/v1"
    
    # API Keys (Required)
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str  # For real-time search
    
    # Optional Keys
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_API_KEY: Optional[str] = None # For LangSmith
    
    # Database Settings
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/travel_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()