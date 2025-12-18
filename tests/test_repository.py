import pytest

from app.repositories.users import UserRepository
from app.schemas.users import UserCreate


@pytest.mark.anyio
async def test_repository_create_and_update(async_session):
    repo = UserRepository(async_session)
    payload = UserCreate(
        telegram_user_id=7, telegram_chat_id=77, timezone="UTC"
    )
    user = await repo.create_or_update(payload)
    assert user.telegram_user_id == 7
    assert user.telegram_chat_id == 77

    # update existing user
    payload2 = UserCreate(
        telegram_user_id=7, telegram_chat_id=777, timezone="Europe/London"
    )
    user2 = await repo.create_or_update(payload2)
    assert user2.telegram_chat_id == 777
    assert user2.timezone == "Europe/London"

    # get by telegram id
    found = await repo.get_by_telegram_user_id(7)
    assert found is not None
    assert found.telegram_chat_id == 777
