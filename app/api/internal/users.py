from fastapi import APIRouter, HTTPException, status

from app.repositories.users import UserRepository
from app.schemas.users import UserRead, UserCreate
from app.core.deps import SessionDep

router = APIRouter(prefix="/internal/users", tags=["internal_users"])


@router.post(
    "/upsert-telegram",
    response_model=UserRead,
    description="Получение Пользователя",
    status_code=status.HTTP_200_OK,
)
async def upsert_telegram_user(
    session: SessionDep,
    payload: UserCreate,
):
    repo = UserRepository(session)
    user = await repo.create_or_update(payload)
    return user


@router.get(
    "/by-telegram/{telegram_user_id}",
    response_model=UserRead,
)
async def get_by_telegram_user_id(session: SessionDep, telegram_user_id: int):
    repo = UserRepository(session)
    user = await repo.get_by_telegram_user_id(telegram_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user
