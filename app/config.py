from pydantic_settings import BaseSettings, SettingsConfigDict
import os


DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV, env_file_encoding='utf-8')
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

settings = Settings()