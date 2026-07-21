from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import Session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session
