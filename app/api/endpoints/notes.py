# app/api/endpoints/notes.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.api.schemas import NoteCreate, NoteRead, NoteUpdate
from app.core.constants import NOTES_TAG
from app.core.db import get_db

router = APIRouter(prefix="/notes", tags=[NOTES_TAG])

@router.post("/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note_endpoint(payload: NoteCreate, db: Session = Depends(get_db)):
    return {
        "id": 1,
        "title": payload.title,
        "content": payload.content,
        "is_public": payload.is_public,
        "is_completed": payload.is_completed,
        "created_at": "2022-01-01T00:00:00.000Z",
    }

@router.get("/", response_model=List[NoteRead])
def list_notes_endpoint(db: Session = Depends(get_db)):
    return [{
        "id": 1,
        "title": "Sample",
        "content": "Mock content",
        "is_public": False,
        "is_completed": False,
        "created_at": "2022-01-01T00:00:00.000Z",
    }]

@router.get("/{note_id}", response_model=NoteRead)
def get_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    if note_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return {
        "id": 1,
        "title": "Sample",
        "content": "Mock content",
        "is_public": False,
        "is_completed": False,
        "created_at": "2022-01-01T00:00:00.000Z",
    }

@router.patch("/{note_id}", response_model=NoteRead)
def update_note_endpoint(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db)):
    if note_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return {
        "id": note_id,
        "title": payload.title or "Sample",
        "content": payload.content or "Mock content",
        "is_public": payload.is_public or False,
        "is_completed": payload.is_completed or False,
        "created_at": "2022-01-01T00:00:00.000Z",
    }

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint(note_id: int, db: Session = Depends(get_db)):
    if note_id != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return