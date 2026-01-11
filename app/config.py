from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Task Management API"
    database_url: str = "sqlite:///./tasks.db"
    debug: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
