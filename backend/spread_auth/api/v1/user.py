from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func, delete
from spread_auth.core.db import get_session, update_object, get_objects, bulk_create_or_update
from spread_auth.core.loggers import get_logger
from spread_auth.core.security import get_current_user, get_password_hash
from spread_auth.models import UserBase, User, UsersPublic, UserPublic, UserCreate, RolePublic, Role, UserRole

router = APIRouter(prefix="/users", tags=["Users"])

logger = get_logger(__name__)

@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=list[UserPublic]
)
async def get_users(session: AsyncSession = Depends(get_session), filters=None, joined=None, order=None,
                    limit: Optional[int] = 20, offset: Optional[int] = 0) -> list[UserPublic]:
    logger.info(f"get_users filters: {filters}")
    result = await get_objects(session, User, limit=limit)
    return result


@router.get(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic
)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> UserPublic:
    db_user = await session.get(User, user_id)
    return db_user


@router.get(
    "/{user_id}/roles/",
    dependencies=[Depends(get_current_user)],
    response_model=list[RolePublic]
)
async def get_role_from_user(
        user_id: int,
        session: AsyncSession = Depends(get_session)
) -> list[RolePublic]:
    # db_role = await session.get(Role, role_id)
    _roles = await get_objects(session, Role, [UserRole.user_id == user_id], [UserRole], limit=None)
    return _roles
    # eturn db_roler

@router.put(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic
)
async def update_user(
        user_id: int,
        user: UserPublic,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
) -> UserPublic:
    try:
        if current_user.id != user_id and not current_user.is_staff:
            raise HTTPException(status_code=403, detail="Access denied")
        user_data = user.model_dump()
        extra_data = {'id': user_id}
        if 'password' in user_data:
            extra_data["hashed_password"] = get_password_hash(user_data['password'])
        db_user = await update_object(session, User, user_id, user, extra_data)
        await session.exec(delete(UserRole).where(UserRole.user_id == user_id))
        await session.commit()
        await bulk_create_or_update(session, UserRole, [UserRole.model_validate(UserRole(user_id=user_id, role_id=_role_id)) for _role_id in  user.roles])
        return db_user
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic
)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_session)
) -> UserPublic:
    try:
        db_obj = User.model_validate(user, update={
            "password": get_password_hash(user.password), 'id': None})
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.delete("/{user_id}")
async def delete_user(user_id: int) -> dict:
    return {}
