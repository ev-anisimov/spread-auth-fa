from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from spread_auth.core.db import get_session, update_object, get_objects, bulk_create_or_update
from spread_auth.core.security import get_current_user, get_password_hash
from spread_auth.models import PermissionBase, Role, RoleBase, RolePublic, User, Permission, PermissionPublic, RolePermissionCnt, RolePermission

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=list[RolePublic]
)
async def get_roles(session: AsyncSession = Depends(get_session), filters=None, joined=None, order=None,
                    limit: Optional[int] = 20, offset: Optional[int] = 0) -> list[RolePublic]:
    result = await get_objects(session, Role, limit=None)
    return result


@router.get(
    "/{role_id}",
    dependencies=[Depends(get_current_user)],
    response_model=RolePublic
)
async def get_role(
        role_id: int,
        session: AsyncSession = Depends(get_session)
) -> RolePublic:
    db_role = await session.get(Role, role_id)
    return db_role


@router.put(
    "/{role_id}",
    dependencies=[Depends(get_current_user)],
    response_model=RolePublic
)
async def update_role(
        role_id: int,
        role: RolePermission,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
) -> RolePublic:
    try:
        if not current_user.is_staff:
            raise HTTPException(status_code=403, detail="Access denied")
        extra_data = {'id': role_id}
        db_user = await update_object(session, Role, role_id, role, extra_data)
        return db_user
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=RolePublic
)
async def create_role(
        role: RoleBase,
        permissions: list[PermissionBase]=Body(...),
        session: AsyncSession = Depends(get_session)
) -> RolePublic:
    try:
        db_obj = Role.model_validate(role, update={'id': None})
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.delete("/{role_id}")
async def delete_role(role_id: int) -> dict:
    return {}


@router.get(
    "/with_count/",
    dependencies=[Depends(get_current_user)],
    response_model=list[RolePermissionCnt]
)
async def get_roles_count(session: AsyncSession = Depends(get_session))->list[RolePermissionCnt]:
    # res = await get_objects(session, Role)
    query = select( Role.id,
            Role.name, func.count(Permission.id).label('cnt')).outerjoin(Permission, Role.id == Permission.role_id).group_by(Role.id)
    result = await session.exec(query)
    return result.all()


@router.get(
    "/{role_id}/with_perms/",
    dependencies=[Depends(get_current_user)],
    response_model=RolePermission
)
async def get_role_with_permissions(
        role_id: int,
        session: AsyncSession = Depends(get_session)
) -> RolePermission:
    # db_role = await session.get(Role, role_id)
    query = select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
    db_role = await session.exec(query)
    db_role = db_role.first()
    return RolePermission(**db_role.model_dump(), permissions=db_role.permissions)
    # eturn db_roler

@router.get(
    "/{role_id}/permissions",
    dependencies=[Depends(get_current_user)],
    response_model=list[PermissionPublic]
)
async def get_permissions_by_role(
        role_id: int,
        project: Optional[int] = None,
        session: AsyncSession = Depends(get_session)
) -> list[PermissionPublic]:
    db_role = await session.get(Role, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Роль не найдена")

    query = select(Permission).where(Permission.role_id == role_id)
    if project:
        query = query.where(Permission.project == project)
    permissions = await session.exec(query)
    return permissions.all()




@router.put(
    "/{role_id}/permissions",
    dependencies=[Depends(get_current_user)],
    response_model=RolePublic
)
async def update_role_with_permissions(
        role_id: int,
        role: RoleBase,
        permissions: list[PermissionBase]=Body(...),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
) -> RolePublic:
    try:
        if not current_user.is_staff:
            raise HTTPException(status_code=403, detail="Access denied")

        extra_data = {'id': role_id}
        db_user = await update_object(session, Role, role_id, role, extra_data)
        _perm = await bulk_create_or_update(session, Permission, permissions)
        return db_user
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
