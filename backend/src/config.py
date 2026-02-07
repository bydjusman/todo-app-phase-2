from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = Field(default="Todo API", json_schema_extra={"alias": "APP_NAME"})
    environment: str = Field(default="development", json_schema_extra={"alias": "ENVIRONMENT"})
    debug: bool = Field(default=True, json_schema_extra={"alias": "DEBUG"})

    # Database
    database_host: str = Field(default="localhost", json_schema_extra={"alias": "DATABASE_HOST"})
    database_port: int = Field(default=5432, json_schema_extra={"alias": "DATABASE_PORT"})
    database_name: str = Field(default="todo_app", json_schema_extra={"alias": "DATABASE_NAME"})
    database_user: str = Field(default="postgres", json_schema_extra={"alias": "DATABASE_USER"})
    database_password: str = Field(default="password", json_schema_extra={"alias": "DATABASE_PASSWORD"})
    database_url: str = Field(default="", json_schema_extra={"alias": "DATABASE_URL"})

    @property
    def async_database_url(self) -> str:
        """Get async database URL for SQLAlchemy."""
        if self.database_url:
            # Remove query parameters for asyncpg (ssl is handled via connect_args)
            base_url = self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return base_url.split("?")[0]
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    @property
    def sync_database_url(self) -> str:
        """Get sync database URL for Alembic migrations."""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )

    # JWT Authentication
    secret_key: str = Field(default="your-secret-key-change-in-production", json_schema_extra={"alias": "SECRET_KEY"})
    algorithm: str = Field(default="HS256", json_schema_extra={"alias": "ALGORITHM"})
    access_token_expire_minutes: int = Field(default=15, json_schema_extra={"alias": "ACCESS_TOKEN_EXPIRE_MINUTES"})
    refresh_token_expire_days: int = Field(default=7, json_schema_extra={"alias": "REFRESH_TOKEN_EXPIRE_DAYS"})

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        json_schema_extra={"alias": "CORS_ORIGINS"}
    )

    # Password hashing
    bcrypt_rounds: int = Field(default=12, json_schema_extra={"alias": "BCRYPT_ROUNDS"})

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
        case_sensitive=False,
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
