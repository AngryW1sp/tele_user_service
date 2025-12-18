import pytest

from app.core.config import settings


@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_auth_required(client):
    payload = {
        "telegram_user_id": 1,
        "telegram_chat_id": 10,
        "timezone": "UTC",
    }
    r = await client.post("/internal/users/upsert-telegram", json=payload)
    assert r.status_code == 401


@pytest.mark.anyio
async def test_wrong_token(client):
    headers = {"Authorization": "Bearer wrong-token"}
    payload = {
        "telegram_user_id": 2,
        "telegram_chat_id": 20,
        "timezone": "UTC",
    }
    r = await client.post(
        "/internal/users/upsert-telegram", json=payload, headers=headers
    )
    assert r.status_code == 403


@pytest.mark.anyio
async def test_upsert_and_get_user(client):
    headers = {"Authorization": f"Bearer {settings.internal_api_token}"}
    payload = {
        "telegram_user_id": 42,
        "telegram_chat_id": 4242,
        "timezone": "Europe/Moscow",
    }
    r = await client.post(
        "/internal/users/upsert-telegram", json=payload, headers=headers
    )
    assert r.status_code == 200
    data = r.json()
    assert data["telegram_user_id"] == 42

    r2 = await client.get("/internal/users/by-telegram/42", headers=headers)
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["telegram_chat_id"] == 4242


@pytest.mark.anyio
async def test_notify_target_success_and_conflicts(client):
    headers = {"Authorization": f"Bearer {settings.internal_api_token}"}
    # create user with chat id
    payload = {
        "telegram_user_id": 100,
        "telegram_chat_id": 5555,
        "timezone": "UTC",
    }
    r = await client.post(
        "/internal/users/upsert-telegram", json=payload, headers=headers
    )
    assert r.status_code == 200

    r2 = await client.get("/internal/notify/by-telegram/100", headers=headers)
    assert r2.status_code == 200
    data = r2.json()
    assert data["telegram_chat_id"] == 5555

    # use repository via upsert-telegram but telegram_chat_id is required by schema, so create via direct post then patch session
    # Instead, create user with chat id then patch DB directly in repository tests; here verify 404 for missing user
    r3 = await client.get("/internal/notify/by-telegram/9999", headers=headers)
    assert r3.status_code == 404
