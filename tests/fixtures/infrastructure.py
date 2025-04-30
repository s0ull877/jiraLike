import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings import get_settings


settings = get_settings()


engine = create_async_engine(url=settings.database_url, future=True, echo=True, pool_pre_ping=True)


AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(autouse=True, scope="function")
async def init_models(event_loop):
    from src.infrastructure.postgres_db import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def get_db_session() -> AsyncSession:
    session = AsyncSessionFactory()
    try:
        yield session
    finally:
        await session.close()