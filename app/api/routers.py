from fastapi import APIRouter

from app.api.endpoints.notes import router as notes_router
from app.core.constants import NOTES_TAG

api_router = APIRouter(prefix="/api")
api_router.include_router(notes_router, prefix="/notes", tags=[NOTES_TAG])