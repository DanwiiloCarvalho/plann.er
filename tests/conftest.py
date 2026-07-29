import os
import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker
)

from app.main import app
from app.adapters.inbound.api.deps import get_db
from app.adapters.outbound.database.models.base import Base
from app.infrastructure.config import settings

@pytest.fixture(scope="session")
def engine() -> AsyncEngine:
    """
    1 - Fixture da engine com escopo de sessão que utilize a variável de ambiente TEST_DATABASE_URL.
    """
    #test_database_url = os.environ.get("TEST_DATABASE_URL")
    test_database_url = settings.DATABASE_URL
    if not test_database_url:
        raise ValueError("A variável de ambiente TEST_DATABASE_URL não está definida.")
    
    return create_async_engine(test_database_url, echo=False)


@pytest.fixture(scope="session", autouse=True)
async def setup_database(engine: AsyncEngine) -> AsyncGenerator[None, None]:
    """
    2 - Fixture com escopo de sessão e autoexecutável para criar e remover as tabelas do banco de testes.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    3 - Fixture com escopo de teste que ofereça uma sessão assíncrona do banco de dados. 
    Ao final do teste ela deve realizar o rollback automático.
    """
    async with engine.connect() as conn:
        transaction = await conn.begin()
        
        async_session_maker = async_sessionmaker(
            bind=conn,
            class_=AsyncSession,
            expire_on_commit=False,
            join_transaction_mode="create_savepoint"
        )
        
        async with async_session_maker() as session:
            yield session
            
        await transaction.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    4 - Fixture com escopo de teste que ofereça um cliente assíncrono httpx, 
    que sobrescreve a sessão do banco de dados utilizada pelas rotas.
    """
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
        
    app.dependency_overrides.clear()
