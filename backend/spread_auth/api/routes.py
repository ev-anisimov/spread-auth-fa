from fastapi import APIRouter

from spread_auth.core.config import settings
from spread_auth.api.v1 import user
from spread_auth.api import auth

api_router = APIRouter()
api_router.include_router(user.router, prefix=settings.V1_STR)
api_router.include_router(auth.router)
