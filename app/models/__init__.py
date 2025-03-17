from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import Generator
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL)
SessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


async def get_db() -> Generator:
    """
    Create and yield a database async_session.
    Ensures proper closure of the session after use.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
