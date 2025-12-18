"""Модуль авторизации для внутренних API.

Содержит простую проверку Bearer token для внутренних эндпоинтов.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

bearer = HTTPBearer(auto_error=False)


def require_internal_auth(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
):
    """Проверяет, что запрос содержит корректный Bearer токен.

    Выбрасывает HTTP 401 при отсутствии схемы/токена и 403 при неверном токене.
    """
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    if creds.credentials != settings.internal_api_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )
