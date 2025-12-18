"""Схема цели уведомления для внутреннего API.

Предназначена для передачи данных о том, куда и как отправлять уведомление.
"""

from pydantic import BaseModel


class NotifyTarget(BaseModel):
    """Данные назначения уведомления.

    Поля:
        - `telegram_chat_id`: id чата для отправки;
        - `timezone`: временная зона получателя;
        - `is_active`: флаг, можно ли отправлять уведомления.
    """

    telegram_chat_id: int
    timezone: str
    is_active: bool
