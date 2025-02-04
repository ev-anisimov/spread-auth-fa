from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from core.db import get_session, update_object, get_objects
from core.security import get_current_user, get_password_hash
from spread_auth.models.user import UserBase, User, UsersPublic, UserPublic, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=list[UserPublic]
)
async def get_users(session: AsyncSession = Depends(get_session), filters=None, joined=None, order=None,
                    limit: Optional[int] = 20, offset: Optional[int] = 0) -> list[UserPublic]:
    result = await get_objects(session, User)
    return result


@router.get(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic
)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)) -> UserPublic:
    db_user = await session.get(User, user_id)
    return db_user


@router.put(
    "/{user_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic
)
async def update_user(
        user_id: int,
        user: UserBase,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
) -> UserPublic:
    if current_user.id != user_id and not current_user.is_staff:
        raise HTTPException(status_code=403, detail="Access denied")
    user_data = user.model_dump()
    extra_data = {'id': user_id}
    if 'password' in user_data:
        extra_data["hashed_password"] = get_password_hash(user_data['password'])
    db_user = await update_object(session, User, user_id, user, extra_data)
    return db_user


@router.post(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=UserPublic
)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserPublic:
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
