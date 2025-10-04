from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.constants import NOTE_TITLE_MAX_LEN


class NoteBase(BaseModel):
    title: str = Field(..., max_length=NOTE_TITLE_MAX_LEN)
    content: str | None = None
    is_public: bool | None = None
    is_completed: bool | None = None


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: str | None = Field(None, max_length=NOTE_TITLE_MAX_LEN)
    content: str | None = None
    is_public: bool | None = None
    is_completed: bool | None = None


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    is_public: bool
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)