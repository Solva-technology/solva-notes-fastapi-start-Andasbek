from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base import Base
from app.core.constants import NOTE_TITLE_MAX_LEN


class Note(Base):

    title: Mapped[str] = mapped_column(
        String(NOTE_TITLE_MAX_LEN),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        String,
        nullable=False,
        server_default="",
    )
    is_public: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
        index=True,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default="false",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
