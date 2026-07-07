from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.outbound.database.mappers.trip_mapper import TripMapper
from app.adapters.outbound.database.models.trip import Trip as TripModel
from app.domain.entities.trip import Trip as TripDomain
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.trip_repository import TripRepository


class SqlAlchemyTripRepository(TripRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.__db_session = session

    async def get_by_id(self, trip_id: UUID) -> TripDomain | None:
        query = select(TripModel).filter(TripModel.id == trip_id)
        result = await self.__db_session.execute(query)
        trip_found: TripModel | None = result.scalar_one_or_none()

        if not trip_found:
            return None

        return TripMapper.to_domain(trip_found)

    async def save(self, trip: TripDomain) -> None:
        trip_model = TripMapper.to_model(trip)
        await self.__db_session.merge(trip_model)

    async def delete(self, trip: TripDomain) -> None:
        query = select(TripModel).filter(TripModel.id == trip.id)
        result = await self.__db_session.execute(query)
        trip_found: TripDomain | None = result.scalar_one_or_none()

        if not trip_found:
            raise TripNotFoundError(trip.id)

        await self.__db_session.delete(trip_found)
