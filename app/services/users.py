"""Сервисный слой для операций с пользователями.

Сервисы инкапсулируют бизнес-логику и транзакционное поведение.
Роутеры вызывают сервисы, а сервисы используют репозитории.
"""

from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import UserRepository
from app.schemas.users import UserCreate
from app.models.users import User

import logging

from app.services.validation import _validate_payload

logger = logging.getLogger(__name__)


async def upsert_user(session: AsyncSession, payload: UserCreate) -> User:
    """Создать или обновить пользователя и зафиксировать транзакцию.

    Возвращает ORM-объект `User` с обновлёнными полями.
    """
    _validate_payload(payload)
    repo = UserRepository(session)
    existing = await repo.get_by_telegram_user_id(payload.telegram_user_id)
    if existing is None:
        user = await repo.create_or_update(payload)
        await session.commit()
        await session.refresh(user)
        logger.info(
            "created user",
            extra={"telegram_user_id": payload.telegram_user_id},
        )
        return user

    user = await repo.create_or_update(payload)
    if not user.is_active:
        user.is_active = True
    await session.commit()
    await session.refresh(user)
    logger.info(
        "updated user", extra={"telegram_user_id": payload.telegram_user_id}
    )
    return user


async def get_user_by_telegram(
    session: AsyncSession, telegram_user_id: int
) -> Optional[User]:
    """Возвращает пользователя по telegram_user_id или None, если не найден."""
    repo = UserRepository(session)
    return await repo.get_by_telegram_user_id(telegram_user_id)
