"""Зависимости FastAPI для работы с базой данных.

Здесь определён `SessionDep` — типовый алиас для внедрения
асинхронной SQLAlchemy-сессии в эндпоинты.
"""

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.db import get_async_session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
