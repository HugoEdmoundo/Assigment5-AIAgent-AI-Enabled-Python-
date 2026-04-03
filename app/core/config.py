from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Agent API"
    DEBUG: bool = True
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./database.db"
    OPENROUTER_API_KEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
