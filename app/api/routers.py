# app/api/routers.py
from fastapi import APIRouter
from .endpoints import notes

api_router = APIRouter()
api_router.include_router(notes.router)