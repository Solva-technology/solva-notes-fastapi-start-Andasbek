from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.api.routers import api_router
from app.core.constants import API_PREFIX


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Notes App", lifespan=lifespan)
    app.include_router(api_router, prefix=API_PREFIX)
    return app
