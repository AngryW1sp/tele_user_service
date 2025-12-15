from fastapi import FastAPI

from app.api.internal.users import router as users_router


app = FastAPI(title="Telegram User Service")


app.include_router(users_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
