"""Pydantic-схемы для работы с пользователями.

`UserCreate` используется для входных данных при создании/обновлении.
`UserRead` — сериализация модели в ответах API.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Схема входных данных для создания/обновления пользователя."""

    telegram_user_id: int
    telegram_chat_id: int
    timezone: str = Field(default="UTC", max_length=64)


class UserRead(BaseModel):
    """Схема для вывода данных пользователя в API-ответах."""

    id: UUID
    telegram_user_id: int
    telegram_chat_id: int
    timezone: str
    is_active: bool

    class Config:
        from_attributes = True
