from pydantic import BaseModel

class NotifyTarget(BaseModel):
    telegram_chat_id: int
    timezone: str
    is_active: bool

    