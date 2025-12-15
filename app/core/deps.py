from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.db import get_async_session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
