import uuid
from app.application.dto.activity_dto import ActivityResponseDTO
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.output_ports.trip_repository import TripRepository


class GetTripActivitiesUseCase:
    def __init__(
        self,
        trip_repo: TripRepository
    ) -> None:
        self.__trip_repo = trip_repo

    async def execute(self, trip_id: uuid.UUID) -> list[ActivityResponseDTO]:
        trip_found = await self.__trip_repo.get_by_id(trip_id)
        if not trip_found:
            raise TripNotFoundError(trip_id)
        return [ActivityResponseDTO(id=activity.id, title=activity.title, date=activity.date, time=activity.time) for activity in trip_found.activities]
