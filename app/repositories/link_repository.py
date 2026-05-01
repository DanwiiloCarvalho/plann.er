from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from collections.abc import Sequence
from app.repositories.base_repository import BaseRepository
from app.models.link import Link
from uuid import UUID


class LinkRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, Link)

    async def find_links_from_trip(self, trip_id: UUID) -> list[Link]:
        try:
            query = select(Link).filter(Link.trip_id == trip_id)
            links_found: Sequence[Link] = (await self._db_session.execute(query)).scalars().all()
            return list(links_found)
        except SQLAlchemyError as e:
            raise e
