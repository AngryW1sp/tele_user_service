"""API маршруты для внутренних операций с пользователями.

Эндпоинты находятся под префиксом `/internal/users` и требуют
внутренней авторизации (Bearer token).
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import require_internal_auth
from app.schemas.users import UserRead, UserCreate
from app.services.users import upsert_user, get_user_by_telegram
from app.core.deps import SessionDep

router = APIRouter(
    prefix="/internal/users",
    tags=["internal_users"],
    dependencies=[Depends(require_internal_auth)],
)


@router.post(
    "/upsert-telegram",
    response_model=UserRead,
    description="Создать или обновить пользователя по telegram_user_id",
    status_code=status.HTTP_200_OK,
)
async def upsert_telegram_user(
    session: SessionDep,
    payload: UserCreate,
):
    """Создаёт нового пользователя или обновляет существующего.

    Аргументы:
      - `session`: асинхронная сессия SQLAlchemy (внедряется зависимостью).
      - `payload`: данные пользователя (`UserCreate`).

    Возвращает объект `UserRead` с сохранёнными полями.
    """
    try:
        user = await upsert_user(session, payload)
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        )


@router.get(
    "/by-telegram/{telegram_user_id}",
    response_model=UserRead,
)
async def get_by_telegram_user_id(session: SessionDep, telegram_user_id: int):
    """Возвращает пользователя по `telegram_user_id`.

    Если пользователь не найден, возвращает HTTP 404.
    """
    user = await get_user_by_telegram(session, telegram_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user
