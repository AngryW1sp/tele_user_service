"""Модуль инициализации асинхронного подключения к базе данных.

Создаёт движок SQLAlchemy и фабрику сессий, а также предоставляет
зависимость `get_async_session` для использования в FastAPI.
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncIterator:
    """Асимптотическая генератор-зависимость, отдающая сессию.

    Используется в `Depends` для внедрения `AsyncSession` в обработчики.
    """
    async with SessionLocal() as session:
        yield session
