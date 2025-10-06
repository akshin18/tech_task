import secrets
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Healthcare Data Processing API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "healthcare_db"
    SQLALCHEMY_DATABASE_URI: str | None = None

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = []

    # LLM settings for summary generation
    OPENAI_API_KEY: str | None = None
    LLM_MODEL: str = "gpt-3.5-turbo"

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info):
        if isinstance(v, str):
            return v
        # Access values through info.data instead of values
        values = info.data
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_SERVER"),
                path=values.get("POSTGRES_DB", ""),
            )
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
