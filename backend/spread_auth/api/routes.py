from fastapi import APIRouter

from spread_auth.core.config import settings
from spread_auth.api.v1 import user, role, project, permission
from spread_auth.api import auth, options, entity

api_router = APIRouter()
api_router.include_router(user.router, prefix=settings.V1_STR)
api_router.include_router(project.router, prefix=settings.V1_STR)
api_router.include_router(role.router, prefix=settings.V1_STR)
api_router.include_router(permission.router, prefix=settings.V1_STR)
api_router.include_router(auth.router)
api_router.include_router(options.router)
api_router.include_router(entity.router)

