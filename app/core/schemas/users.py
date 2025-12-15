from uuid import UUID

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    telegram_user_id: int
    telegram_chat_id: int
    timezone: str = Field(default="UTC", max_length=64)


class UserRead(BaseModel):
    id: UUID
    telegram_user_id: int
    telegram_chat_id: int
    timezone: str
    is_active: bool

    class Config:
        from_attributes = True
