import os
from typing import Optional

from alembic import command
from alembic.config import Config
from sqlmodel import SQLModel, create_engine, select

from sqlalchemy.orm import selectinload
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
    logger.info(f"init_db dbname: {settings.DATABASE_NAME}")
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


async def get_object_by_id(session: AsyncSession, model_object: SQLModel, obj_id: int):
    db_obj = await session.get(model_object, obj_id)
    return db_obj


async def update_object(session: AsyncSession, model_object: SQLModel, obj_id: int, obj_data: SQLModel, extra_data:dict=None):
    db_obj = await get_object_by_id(session, model_object, obj_id)
    db_obj.sqlmodel_update(obj_data.model_dump(), update=extra_data or {})
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_objects(session: AsyncSession, model_object: SQLModel, filters: Optional[list] = None, joined=None,
                      order=None, limit: Optional[int] = 20, offset: Optional[int] = 0):
    filters = filters or []
    order = order or []

    query = select(model_object)
    if joined:
        query = query.join(*joined).options(selectinload(*joined))
    query = query.where(*filters)
    query = query.limit(limit).offset(offset).order_by(*order)
    res = await session.exec(query)
    return res.all()
