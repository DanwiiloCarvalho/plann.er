from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from app.core.config import settings

async_engine: AsyncEngine = create_async_engine(str(settings.DATABASE_URL))
