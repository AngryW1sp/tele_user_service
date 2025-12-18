"""Модель SQLAlchemy для сущности `User`.

Поля:
  - `telegram_user_id` — уникальный идентификатор пользователя Telegram;
  - `telegram_chat_id` — идентификатор чата (может быть None);
  - `timezone` — временная зона пользователя;
  - `is_active` — флаг активности; временные метки `created_at`/`updated_at`.
"""

import uuid
from datetime import datetime, timezone

from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer, String, Boolean, DateTime


class User(Base):
    """ORM-модель пользователя.

    Экземпляры этой модели используются репозиторием для CRUD-операций.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    telegram_user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
        index=True,
    )

    telegram_chat_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        default="UTC",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
