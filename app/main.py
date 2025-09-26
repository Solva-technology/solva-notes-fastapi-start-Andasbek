# app/main.py
from fastapi import FastAPI
from app.api.routers import api_router
from app.core.constants import API_PREFIX

def create_app() -> FastAPI:
    app = FastAPI(title="FastAPI Notes App")
    app.include_router(api_router, prefix=API_PREFIX)
    return app