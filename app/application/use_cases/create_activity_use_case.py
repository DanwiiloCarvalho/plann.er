import uuid

from app.application.dto.activity_dto import ActivityDTO, ActivityResponseDTO
from app.domain.entities.activity import Activity
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.trip_repository import TripRepository
from app.domain.ports.unit_of_work import UnitOfWork


class CreateActivityUseCase:
    def __init__(
        self,
        trip_repo: TripRepository,
        uow: UnitOfWork
    ) -> None:
        self.__trip_repo = trip_repo
        self.__uow = uow

    async def execute(self, trip_id: uuid.UUID, activity: ActivityDTO) -> ActivityResponseDTO:
        async with self.__uow:
            trip_found = await self.__trip_repo.get_by_id(trip_id)
            if not trip_found:
                raise TripNotFoundError(trip_id)
            new_activity = Activity(
                id=uuid.uuid1(),
                title=activity.title,
                date=activity.date,
                time=activity.time
            )
            trip_found.activities = new_activity
            await self.__trip_repo.save(trip_found)
            return ActivityResponseDTO(
                id=new_activity.id,
                title=new_activity.title,
                date=new_activity.date,
                time=new_activity.time
            )
