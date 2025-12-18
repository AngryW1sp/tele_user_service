"""База для декларативных моделей SQLAlchemy.

Наследуйте все ORM-модели от `Base`.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Декларативный базовый класс для моделей."""

    pass
