from app.schemas.users import UserCreate


def _validate_payload(payload: UserCreate) -> None:
    if not getattr(payload, "telegram_user_id", None):
        raise ValueError("telegram_user_id is required in payload")
