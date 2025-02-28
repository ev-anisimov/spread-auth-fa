from fastapi import APIRouter, Depends, HTTPException
from core.config import FileConfig
from core.security import get_current_user
from spread_auth.models import Options, User

router = APIRouter(prefix="/options", tags=["Options"])


@router.get(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=Options,
)
async def get_options() :
    return Options.model_validate(FileConfig().to_json())

@router.put(
    "/",
    dependencies=[Depends(get_current_user)],
    response_model=Options
)
async def update_options(
        file_config_data:Options,
        current_user: User = Depends(get_current_user)
):
    try:
        if not current_user.is_staff:
            raise HTTPException(status_code=403, detail="Access denied")
        FileConfig().update(file_config_data)
        return Options.model_validate(FileConfig().to_json())
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
