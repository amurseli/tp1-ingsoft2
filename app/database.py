import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('DATABASE_USER', 'admin')}:"
    f"{os.getenv('DATABASE_PASSWORD', 'password')}@"
    f"{os.getenv('DATABASE_HOST', 'db')}:"
    f"{os.getenv('DATABASE_PORT', '5432')}/"
    f"{os.getenv('DATABASE_NAME', 'db')}"
)

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session and close it after use."""
    async with AsyncSessionLocal() as session:
        yield session