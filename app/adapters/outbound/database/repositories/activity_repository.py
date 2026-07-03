from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.adapters.outbound.database.mappers.activity_mapper import ActivityMapper
from app.adapters.outbound.database.models.activity import Activity as ActivityModel
from app.domain.entities.activity import Activity as ActivityDomain
from collections.abc import Sequence
from app.adapters.outbound.database.repositories.base_repository import BaseRepository
from uuid import UUID


class ActivityRepository(BaseRepository[ActivityModel, ActivityDomain]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, ActivityModel, ActivityMapper)

    async def find_activities_from_trip_id(self, trip_id: UUID) -> list[ActivityDomain]:
        query = select(self._model_cls).filter(
            self._model_cls.trip_id == trip_id)
        result = await self._db_session.execute(query)
        activities_found: Sequence[ActivityModel] = result.scalars().all()
        return [self._mapper.to_domain(activity) for activity in activities_found]
