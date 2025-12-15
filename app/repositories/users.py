from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate
from app.models.users import User
from sqlalchemy import select


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_user_id(
        self,
        telegram_user_id: int,
    ) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        return result.scalar_one_or_none()

    async def create_or_update(
        self,
        data: UserCreate,
    ):
        user = await self.get_by_telegram_user_id(data.telegram_user_id)
        if user:
            user.telegram_chat_id = data.telegram_chat_id
            user.timezone = data.timezone
        else:
            user = User(
                telegram_user_id=data.telegram_user_id,
                telegram_chat_id=data.telegram_chat_id,
                timezone=data.timezone,
            )
            self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
