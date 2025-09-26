from sqlalchemy.orm import Session
from typing import Any, Optional, Sequence

def create_note(db: Session, data: Any) -> Any:
    pass

def get_note(db: Session, note_id: int) -> Optional[Any]:
    pass

def get_notes(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Any]:
    pass

def update_note(db: Session, note_id: int, data: Any) -> Optional[Any]:
    pass

def delete_note(db: Session, note_id: int) -> Optional[Any]:
    pass
