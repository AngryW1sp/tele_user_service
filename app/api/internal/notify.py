"""Маршруты для получения цели уведомления по telegram_user_id.

Эндпоинты возвращают структуру `NotifyTarget`, содержащую данные
для отправки уведомления (telegram_chat_id, timezone, is_active).
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import require_internal_auth
from app.core.deps import SessionDep
from app.repositories.users import UserRepository
from app.schemas.notify import NotifyTarget

router = APIRouter(
    prefix="/internal/notify",
    tags=["internal-notify"],
    dependencies=[Depends(require_internal_auth)],
)


@router.get("/by-telegram/{telegram_user_id}", response_model=NotifyTarget)
async def get_notify_target_by_telegram(
    telegram_user_id: int,
    session: SessionDep,
):
    """Возвращает `NotifyTarget` для указанного `telegram_user_id`.

    Поведения:
      - 404 если пользователь не найден;
      - 409 если у пользователя отсутствует `telegram_chat_id`.
    """
    user = await UserRepository(session).get_by_telegram_user_id(
        telegram_user_id
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user.telegram_chat_id is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User does not have a telegram_chat_id",
        )
    return NotifyTarget(
        telegram_chat_id=user.telegram_chat_id,
        timezone=user.timezone,
        is_active=user.is_active,
    )
