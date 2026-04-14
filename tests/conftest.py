from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models import _all_models
import pytest

DATABASE_URL: str = str(settings.DATABASE_URL)


@pytest.fixture
async def db_session():
    async_engine: AsyncEngine = create_async_engine(url=DATABASE_URL)
    Session = async_sessionmaker(bind=async_engine, expire_on_commit=False)

    async with Session() as db_session:
        yield db_session
