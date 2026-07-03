from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence
from app.adapters.outbound.database.mappers.trip_mapper import TripMapper
from app.adapters.outbound.database.models.trip import Trip as TripModel
from app.adapters.outbound.database.repositories.base_repository import BaseRepository
from uuid import UUID

from app.domain.entities.trip import Trip as TripDomain
from app.domain.exceptions.entity_not_found import EntityNotFoundError


class TripRepository(BaseRepository[TripModel, TripDomain]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, TripModel, TripMapper)

    async def get_trips_by_owner_name(self, owner_name: str) -> list[TripDomain]:
        query = select(self._model_cls).filter(
            self._model_cls.owner_name == owner_name)
        result = await self._db_session.execute(query)
        trips_founded: Sequence[TripModel] = result.unique().scalars().all()
        return [self._mapper.to_domain(trip) for trip in trips_founded]

    async def confirm_trip(self, trip_id: UUID) -> TripDomain:
        query = select(self._model_cls).filter(self._model_cls.id == trip_id)
        result = await self._db_session.execute(query)
        trip_found: TripModel | None = result.scalar_one_or_none()

        if not trip_found:
            raise EntityNotFoundError(trip_id)

        trip_found.status = True
        return self._mapper.to_domain(trip_found)
