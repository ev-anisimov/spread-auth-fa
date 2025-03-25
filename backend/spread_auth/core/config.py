import json
import os
import secrets
from typing import Any, Literal
from pathlib import Path, PurePath

from pydantic import (
    Field,
    PostgresDsn,
    computed_field,
    BaseModel,
)
from pydantic_core import MultiHostUrl, from_json
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv, find_dotenv

from spread_auth.core.singleton import BaseSingleton, SingletonMeta

load_dotenv(find_dotenv('.env'))


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)

def read_file_config():
    if settings.CONFIG_FILE.exists():
        with settings.CONFIG_FILE.open('r') as f:
            return json.load(f)
    return {}

def write_file_config(_data:dict):
    settings.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    settings.CONFIG_FILE.write_text(json.dumps(_data, indent=4))


class FileConfig:
    """Pydantic-модель с поддержкой Singleton и загрузки из файла."""
    name:str = None
    project_id:int = None
    _instance = None  # Для хранения Singleton

    def __new__(cls, *args, **kwargs):
        """Гарантирует, что всегда возвращается один и тот же объект."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.reload()  # Загружаем данные при первом создании
        return cls._instance

    def reload(self):
        """Перезаписывает данные из файла конфигурации."""
        _data = read_file_config()
        self.name = _data.get("name")
        self.project_id = _data.get("project_id")

    def update(self, _data):
        self.__dict__.update(_data)
        self.save()

    def save(self):
        """Сохраняет текущий конфиг в файл."""
        write_file_config(self.to_json())

    def to_json(self) -> dict:
        """
        Сериализовать поля синглтона в json
        """
        # res = {
        #     'name': self.name,
        #     'project_id': self.project_id,
        # }
        return self.__dict__

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        extra="ignore",
    )
    STATIC_DIR:str = "/static/"
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


    CONFIG_PATH: str = str(Path('/', 'var', 'project'))
    CONFIG_FILE_NAME: str = 'auth.json'

    ENTITY_PATH: str = str(Path('/', 'var', 'project'))
    ENTITY_FILE_NAME: str = 'entity.json'

    @computed_field
    @property
    def CONFIG_FILE(self) -> Path:
        return Path(self.CONFIG_PATH) / self.CONFIG_FILE_NAME

    @computed_field
    @property
    def ENTITY_FILE(self) -> Path:
        return Path(self.ENTITY_PATH) / self.ENTITY_FILE_NAME

    @computed_field
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

    @computed_field
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
# file_config = FileConfig()
# file_config.reload()