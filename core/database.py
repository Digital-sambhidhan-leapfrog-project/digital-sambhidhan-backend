from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    """
    Get a database session.

    Yields:
        Session: SQLAlchemy database session.

    Usage:
        ```
        with get_db() as db:
            # Perform database operations
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
