from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    database_url: str = "postgresql://guild_master:SecurePassword123!@localhost:5433/quest_academy_lms"
    
    # JWT
    secret_key: str = "your-super-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # App
    app_name: str = "Quest Academy LMS"
    debug: bool = True
    
    # Game Settings
    xp_per_level: int = 1000  # XP needed per level
    base_hp: int = 100
    hp_per_level: int = 10
    
    # AI Config
    openrouter_api_key: str = "sk-or-v1-..."
    ai_model: str = "google/gemini-pro"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
