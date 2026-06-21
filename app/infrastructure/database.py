from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.infrastructure.config import settings

async_engine: AsyncEngine = create_async_engine(str(settings.DATABASE_URL))
Session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
