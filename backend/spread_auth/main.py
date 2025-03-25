import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator
import os
import signal

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.loggers import get_logger
from core.utils import fill_cache_permission_for_users
from spread_auth.core.middleware import LoggingMiddleware
from spread_auth.core.db import init_db
from spread_auth.core.config import settings
from spread_auth.api import routes

logger = get_logger(__name__)

logger.info(f"START STATISTICS".center(104, '*'))
logger.info(f"get_settings data: {settings}")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await init_db()
    loop = asyncio.get_event_loop()
    loop.create_task(fill_cache_permission_for_users())
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.include_router(routes.api_router, prefix="/api")

def shutdown_event(_signal, frame):
    logger.info(f"shutdown_event")
    os.kill(os.getpid(), signal.SIGTERM)
    logger.info(f"Приложение завершено {_signal}")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )

signal.signal(signal.SIGQUIT, shutdown_event)
signal.signal(signal.SIGINT, shutdown_event)

# app.mount(
#     '/',
#     StaticFiles(directory=settings.STATIC_DIR, html=True),
#     name='static'
# )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
