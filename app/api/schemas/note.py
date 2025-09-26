# app/api/schemas/note.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class NoteBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    is_public: bool = False
    is_completed: bool = False

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    content: str | None = None
    is_public: bool | None = None
    is_completed: bool | None = None

class NoteRead(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime