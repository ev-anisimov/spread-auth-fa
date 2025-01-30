import secrets
from typing import Any, Literal

from pydantic import (
    Field,
    PostgresDsn,
    computed_field,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


# DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        extra="ignore",
    )
    V1_STR: str = "/v1"

    # openssl rand -hex 32
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 3 days = 3 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3
    ALGORITHM: str = "HS256"

    FRONTEND_HOST: str = "http://localhost:8080"

    PROJECT_NAME: str
    LOG_LEVEL: Literal[
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL',
        'FATAL',
    ] = Field('INFO', label='Уровень логирования')

    DATABASE_SERVER: str
    DATABASE_PORT: int = 5432
    DATABASE_USER: str
    DATABASE_PASSWORD: str = ""
    DATABASE_NAME: str = ""

    # ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    #     ]


    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_SYNC_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )

    # class Config:
    #     env_file = ".env"
    # BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = []
    #
    # @computed_field  # type: ignore[prop-decorator]
    # @property
    # def all_cors_origins(self) -> list[str]:
    #     return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
    #         self.FRONTEND_HOST


# try:
#     settings = Settings()
#     print("Settings loaded successfully:", settings.dict())
# except Exception as e:
#     print("Error loading settings:", e)

settings = Settings()
