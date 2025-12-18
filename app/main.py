"""Основной модуль приложения FastAPI.

Здесь создаётся экземпляр `FastAPI`, подключаются внутренние роутеры
и определяются общие служебные эндпоинты.
"""

from fastapi import FastAPI

from app.api.internal.users import router as users_router
from app.api.internal.notify import router as notify_router


app = FastAPI(title="Telegram User Service")


app.include_router(users_router)
app.include_router(notify_router)


@app.get("/health")
async def health():
    """Проверочный эндпоинт статуса приложения.

    Возвращает простой JSON со статусом для healthchecks.
    """
    return {"status": "ok"}
