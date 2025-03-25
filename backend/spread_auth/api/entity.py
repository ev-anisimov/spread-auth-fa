import json
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from sqlmodel import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from spread_auth.core.db import get_session, get_objects
from spread_auth.core.utils import generate_entities
from spread_auth.core.config import settings
from spread_auth.core.security import get_current_user
from spread_auth.models import User, Entity, EntityObjectType

router = APIRouter(prefix="/entity", tags=["Entity"])


@router.post(
    "/load/",
    dependencies=[Depends(get_current_user)],
)
async def load_entity(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
) -> JSONResponse:
    try:
        if not current_user.is_staff:
            raise HTTPException(status_code=403, detail="Access denied")

        if settings.ENTITY_FILE.exists():
            with settings.ENTITY_FILE.open("r") as f:
                _file = json.load(f)
            for project_id, project_data in _file.items():
                # on_del = await get_objects(session, Entity,[Entity.project_id==project_id])
                query = delete(Entity).where(Entity.project_id == int(project_id))
                await session.exec(query)
                await session.commit()
                await generate_entities(session, project_id, project_data)

                # session.add_all(_entities)
                # await session.commit()  # Один запрос на сохранение в БД
        else:
            raise HTTPException(status_code=500, detail=f'File not found {settings.ENTITY_FILE.name}')
        return JSONResponse(status_code=200, content={'load': 'success'})
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.get("/locations/",
    dependencies=[Depends(get_current_user)],
    response_model=list[Entity])
async def get_locations(
        project: Optional[int] = None,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
)->list[Entity]:
    try:
        _filters=[Entity.obj_type==EntityObjectType.Location]
        result = await get_objects(session, Entity, _filters, limit=None)
        return result
    except Exception as ex:
        print(ex)

@router.get("/type_subginery/",
    dependencies=[Depends(get_current_user)],
    response_model=list[Entity])
async def get_type_subginery(
        project: Optional[int] = None,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
)->list[Entity]:
    try:
        _filters = [Entity.obj_type == EntityObjectType.TypeSubginery]
        result = await get_objects(session, Entity, _filters, limit=None)
        return result
    except Exception as ex:
        print(ex)


@router.get("/type_enginery/",
    dependencies=[Depends(get_current_user)],
    response_model=list[Entity])
async def get_type_enginery(
        project: Optional[int] = None,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
)->list[Entity]:
    try:
        _filters = [Entity.obj_type == EntityObjectType.TypeEnginery]
        result = await get_objects(session, Entity, _filters,limit=None)
        return result
    except Exception as ex:
        print(ex)


@router.get("/enginery/",
    dependencies=[Depends(get_current_user)],
    response_model=list[Entity])
async def get_enginery(
        project: Optional[int] = None,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
)->list[Entity]:
    try:
        _filters = [Entity.obj_type == EntityObjectType.Enginery]
        result = await get_objects(session, Entity, _filters, limit=None)
        return result
    except Exception as ex:
        print(ex)
