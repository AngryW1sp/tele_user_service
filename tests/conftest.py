import sys
import os

# Ensure project root is on sys.path so `import app` works when running tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest # noqa: E402

from httpx import AsyncClient, ASGITransport # noqa: E402
from sqlalchemy.ext.asyncio import ( # noqa: E402
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import event # noqa: E402

from app.main import app # noqa: E402
from app.models.base import Base # noqa: E402
from app.core.db import get_async_session  # noqa: E402


DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(DATABASE_URL, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="session")
async def connection(engine):
    """Устанавливает единую соединение/транзакцию на сессию тестов.

    Мы открываем соединение и начинаем внешнюю транзакцию, которая будет
    откатана после выполнения всех тестов.
    """
    conn = await engine.connect()
    trans = await conn.begin()
    try:
        yield conn
    finally:
        await trans.rollback()
        await conn.close()


@pytest.fixture
async def async_session(connection):
    """Фикстура сессии для каждого теста с вложенной транзакцией.

    Создаём `AsyncSession`, начинаем `begin_nested()` (SAVEPOINT) и
    регистрируем слушатель `after_transaction_end`, чтобы при завершении
    вложенной транзакции автоматически восстанавливать новый SAVEPOINT.
    После теста сессия закрывается, а внешняя транзакция (в fixture `connection`)
    будет откатана при завершении сессии тестов.
    """
    maker = async_sessionmaker(
        bind=connection, class_=AsyncSession, expire_on_commit=False
    )
    async with maker() as session:
        await session.begin_nested()

        # SQLAlchemy синхронный слушатель для восстановления SAVEPOINT после коммита
        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(sess, trans):
            # Если транзакция была завершена и сессия всё ещё активна,
            # начинаем новую вложенную транзакцию (SAVEPOINT).
            if not sess.is_active:
                return
            try:
                sess.begin_nested()
            except Exception:
                pass

        yield session


@pytest.fixture
async def client(async_session):
    async def _override_get_session():
        yield async_session

    app.dependency_overrides[get_async_session] = _override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_async_session, None)
