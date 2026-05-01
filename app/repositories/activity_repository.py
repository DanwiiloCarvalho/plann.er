from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.models.activity import Activity
from collections.abc import Sequence
from app.repositories.base_repository import BaseRepository
from uuid import UUID


class ActivityRepository(BaseRepository):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, Activity)

    async def find_activities_from_trip(self, trip_id: UUID) -> list[Activity]:
        try:
            query = select(Activity).filter(Activity.trip_id == trip_id)
            activities_found: Sequence[Activity] = (await self._db_session.execute(query)).scalars().all()
            return list(activities_found)
        except SQLAlchemyError as e:
            raise e
