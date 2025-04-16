from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    # FastAPI Configuration
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # MongoDB Configuration
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str

    # Mongo-Express Configuration
    ME_CONFIG_BASICAUTH_PASSWORD: str
    ME_CONFIG_BASICAUTH_USERNAME: str
    ME_CONFIG_MONGODB_ENABLE_ADMIN: str
    ME_CONFIG_MONGODB_PORT: int
    ME_CONFIG_MONGODB_SERVER: str
    ME_CONFIG_OPTIONS_EDITORTHEME: str
    ME_CONFIG_MONGODB_AUTH_DATABASE: str
    ME_CONFIG_MONGODB_AUTH_USERNAME: str
    ME_CONFIG_MONGODB_AUTH_PASSWORD: str
    ME_CONFIG_SITE_SESSIONSECRET: str
    ME_CONFIG_MONGODB_URL: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
