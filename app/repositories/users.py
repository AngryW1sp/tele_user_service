"""Репозиторий для работы с моделью `User`.

Содержит методы для поиска и создания/обновления пользователей в БД.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate
from app.models.users import User
from sqlalchemy import select


class UserRepository:
    """Класс-репозиторий для операций с `User`.

    Аргументы конструктора:
      - `session`: асинхронная сессия SQLAlchemy.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_user_id(
        self,
        telegram_user_id: int,
    ) -> User | None:
        """Возвращает пользователя по `telegram_user_id` или `None`.

        Использует `select` для выполнения запроса.
        """
        result = await self.session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        data: UserCreate,
    ):
        """Создаёт нового пользователя или обновляет существующего.
        Если пользователь с указанным `telegram_user_id` уже существует,
        обновляет его поля `telegram_chat_id` и `timezone`."""
        user = await self.get_by_telegram_user_id(data.telegram_user_id)
        if user:
            user.telegram_chat_id = data.telegram_chat_id
            user.timezone = data.timezone
        if user:
            # Если payload не содержит telegram_chat_id (None), не перезаписываем
            # существующее значение.
            if data.telegram_chat_id is not None:
                user.telegram_chat_id = data.telegram_chat_id
            user.timezone = data.timezone
        else:
            user = User(
                telegram_user_id=data.telegram_user_id,
                telegram_chat_id=data.telegram_chat_id,
                timezone=data.timezone,
            )
            self.session.add(user)

        return user
