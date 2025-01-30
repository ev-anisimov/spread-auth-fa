import os
from alembic import command
from alembic.config import Config
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy_utils import database_exists, create_database
from core.config import settings
from core.loggers import get_logger

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

async_session = async_sessionmaker(engine,
                                   class_=AsyncSession,
                                   # autocommit=True,
                                   expire_on_commit=False,
                                   autoflush=False,
                                   # autobegin=False
                                   )

logger = get_logger(__name__)

def run_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")

async def init_db():
    """Инициализация базы данных. Создание при отсутствии. Применение миграций"""
    logger.info(f"init_db {settings.DATABASE_NAME}")
    sync_engine = create_engine(str(settings.SQLALCHEMY_DATABASE_SYNC_URI))
    try:
        if not database_exists(sync_engine.url):
            create_database(sync_engine.url)
    except Exception as ex:
        logger.exception(ex)

    async with engine.begin() as connection:
        try:
            logger.info(f"init_db migrate run")
            # cfg = Config("../.././alembic.ini")
            cfg = Config('/home/egor/Repository/spread-auth-fa/backend/alembic.ini')
            await connection.run_sync(run_upgrade, cfg)
            # cfg.attributes["connection"] = connection
            # command.upgrade(cfg, "head")
            logger.info(f"init_db migrate end")
        except Exception as ex:
            logger.exception(ex)


async def get_session() -> AsyncSession:
    """for Depends"""
    async with async_session() as session:
        yield session
