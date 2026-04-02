from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.database import async_engine

Session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
