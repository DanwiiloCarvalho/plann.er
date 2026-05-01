from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence
from app.models.trip import Trip
from app.repositories.base_repository import BaseRepository
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError


class TripRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, Trip)

    async def get_by_owner_name(self, owner_name: str) -> list[Trip]:
        try:
            query = select(Trip).filter(Trip.owner_name == owner_name)
            result = await self._db_session.execute(query)
            trip_founded: Sequence[Trip] = result.unique().scalars().all()
            return list(trip_founded)
        except SQLAlchemyError as e:
            raise e

    async def confirm_trip(self, trip_id: UUID) -> Trip | None:
        try:
            query = select(Trip).filter(Trip.id == trip_id)
            result = await self._db_session.execute(query)
            trip_found: Trip | None = result.unique().scalar_one_or_none()

            if not trip_found:
                return None

            trip_found.status = True
            await self._db_session.commit()
            return trip_found
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise e
