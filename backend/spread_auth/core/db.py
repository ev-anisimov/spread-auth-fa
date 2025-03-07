import os
from typing import Optional

from alembic import command
from alembic.config import Config
from sqlmodel import SQLModel, create_engine, select, update, insert, case

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


async def update_object(session: AsyncSession, model_object: SQLModel, obj_id: int, obj_data: SQLModel,
                        extra_data: dict = None):
    db_obj = await get_object_by_id(session, model_object, obj_id)
    db_obj.sqlmodel_update(obj_data.model_dump(), update=extra_data or {})
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def bulk_create(session: AsyncSession, model_object: SQLModel, objects_data: list[SQLModel], returning=None):
    try:
        _ins = insert(model_object).values([obj.model_dump(exclude_unset=True) for obj in objects_data])
        if returning:
            _ins = _ins.returning(model_object)
        res = await session.exec(_ins)
        await session.commit()
        return res.all() if returning else []
    except Exception as ex:
        logger.exception(ex)


async def bulk_update(session: AsyncSession, model_object: SQLModel, objects_data: list[SQLModel], returning=None):
    try:
        query = update(model_object)
        # используем deprecated execute потому что обычный exec не может в массовое обновление
        await session.execute(query, [obj.model_dump(exclude_unset=True) for obj in objects_data])
        await session.commit()
        if returning:
            # Формируем объекты типа entity из входных данных
            updated_entities = [model_object.model_validate(obj.model_dump()) for obj in objects_data]
            return  updated_entities

    except Exception as ex:
        logger.exception(ex)


async def bulk_create_or_update(session: AsyncSession, model_object: SQLModel, objects_data: list[SQLModel]) -> list[
                                                                                                                    SQLModel] | None:
    _to_update, _to_create = [], []
    for obj_data in objects_data:
        if obj_data.id:
            _to_update.append(obj_data)
        else:
            _to_create.append(obj_data)

    inserted_rs, updated_rs = [], []
    if _to_create:
        inserted_rs = await bulk_create(session, model_object, _to_create, returning=True)
    if _to_update:
        updated_rs = await bulk_update(session, model_object, _to_update, returning=True)
    return list(set(inserted_rs + updated_rs))


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
