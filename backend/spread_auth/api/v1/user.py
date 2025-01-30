from fastapi import APIRouter

from spread_auth.models.user import UserBase



router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_users():
    # some async operation could happen here
    # example: `data = await get_all_datas()`
    l = []
    for i in range(50):
        l.append(
            {'id': i,
             'first_name': f'first_name{i}',
             'name': f'name{i}',
             'last_name': f'last_name{i}',
             'username': f'username{i}',
             })
    return l


@router.get("/{user_id}")
async def get_user(user_id: int)->UserBase:
    return UserBase(**{'id': user_id,
            'first_name': f'first_name{user_id}',
            'name': f'name{user_id}',
            'last_name': f'last_name{user_id}',
            'username': f'username{user_id}',
            })

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserBase)->UserBase:
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int)->dict:
    return {}