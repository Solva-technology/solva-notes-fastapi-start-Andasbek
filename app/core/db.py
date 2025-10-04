from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_session() -> Generator[Session, None, None]:
    """Зависимость для FastAPI: выдаёт сессию и корректно закрывает её."""
    with SessionFactory() as session:
        yield session
