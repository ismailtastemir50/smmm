from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./depo_erp.db"
    SECRET_KEY: str = "depo-erp-2026-gizli"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()