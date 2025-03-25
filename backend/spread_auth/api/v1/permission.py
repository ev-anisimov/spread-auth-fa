from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from core.cache import PermissionUsersCache
from core.db import get_session, update_object, get_objects
from core.security import get_current_user
from core.utils import get_permission_for_user
from spread_auth.models import Project, ProjectBase, ProjectPublic, ProjectPublicCount, Permission, User

router = APIRouter(tags=["Permission"])

@router.get("/get_perms/",
    dependencies=[Depends(get_current_user)])
async def get_perms(
        project: Optional[int],
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    _key =f'{current_user.id}/{project}'
    perms = PermissionUsersCache().get(_key)
    if not perms:
        perms = await get_permission_for_user(session, current_user, project)
        PermissionUsersCache().set(_key, perms)
    return JSONResponse(perms)
