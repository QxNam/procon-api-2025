from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Procon 2025"
    POSTGRES_URL: str = "postgresql+asyncpg://admin:admin@localhost:5432/procondb"
    JWT_SECRET_KEY: str = "supersecret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/system.log"

    class Config:
        env_file = ".env"

settings = Settings()
