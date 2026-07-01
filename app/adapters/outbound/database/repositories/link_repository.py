from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence
from app.adapters.outbound.database.mappers.link_mapper import LinkMapper
from app.adapters.outbound.database.repositories.base_repository import BaseRepository
from app.adapters.outbound.database.models.link import Link as LinkModel
from app.domain.entities.link import Link as LinkDomain
from uuid import UUID


class LinkRepository(BaseRepository[LinkModel, LinkDomain]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, LinkModel, LinkMapper)

    async def find_links_from_trip_id(self, trip_id: UUID) -> list[LinkDomain]:
        query = select(self._model_cls).filter(
            self._model_cls.trip_id == trip_id)
        result = await self._db_session.execute(query)
        links_found: Sequence[LinkModel] = result.scalars().all()

        return [self._mapper.to_domain(link) for link in list(links_found)]
