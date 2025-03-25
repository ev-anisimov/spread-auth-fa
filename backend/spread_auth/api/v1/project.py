from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from core.db import get_session, update_object, get_objects
from core.security import get_current_user
from spread_auth.models import Project, ProjectBase, ProjectPublic, ProjectPublicCount, Permission, User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=list[ProjectPublic]
)
async def get_projects(session: AsyncSession = Depends(get_session), filters=None, joined=None, order=None,
                       limit: Optional[int] = 20, offset: Optional[int] = 0) -> list[ProjectPublic]:
    result = await get_objects(session, Project, limit=None)
    return result


@router.get(
    "/with_count/",
    dependencies=[Depends(get_current_user)],
    response_model=list[ProjectPublicCount]
)
async def get_projects(session: AsyncSession = Depends(get_session), filters=None, joined=None, order=None,
                       limit: Optional[int] = 20, offset: Optional[int] = 0) -> list[ProjectPublic]:
    query = select(Project.id, Project.name, Project.type, Project.connection_params, Project.project_id,
                   func.count(Permission.id).label('cnt')).outerjoin(Permission,
                                                                     Project.project_id == Permission.project).group_by(
        Project.id)
    result = await session.exec(query)
    return result.all()


@router.get(
    "/{project_id}",
    dependencies=[Depends(get_current_user)],
    response_model=ProjectPublic
)
async def get_project(project_id: int, session: AsyncSession = Depends(get_session)) -> ProjectPublic:
    db_project = await session.get(Project, project_id)
    return db_project


@router.put(
    "/{project_id}",
    dependencies=[Depends(get_current_user)],
    response_model=ProjectPublic
)
async def update_project(
        project_id: int,
        project: ProjectBase,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
) -> ProjectPublic:
    try:
        if not current_user.is_staff:
            raise HTTPException(status_code=403, detail="Access denied")
        extra_data = {'id': project_id}
        db_project = await update_object(session, Project, project_id, project, extra_data)
        return db_project
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=ProjectPublic
)
async def create_project(project: ProjectBase, session: AsyncSession = Depends(get_session)) -> ProjectPublic:
    try:
        db_obj = Project.model_validate(project, update={'id': None})
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.delete("/{project_id}")
async def delete_project(project_id: int) -> dict:
    return {}
