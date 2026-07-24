import uuid

from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.trip_repository import TripRepository
from app.domain.ports.unit_of_work import UnitOfWork


class ConfirmParticipationUseCase:
    def __init__(
        self,
        trip_repo: TripRepository,
        uow: UnitOfWork
    ) -> None:
        self.__trip_repo = trip_repo
        self.__uow = uow

    async def execute(
        self,
        trip_id: uuid.UUID,
        email_to_invite_id: uuid.UUID,
        fullname: str
    ) -> None:
        async with self.__uow:
            trip_found = await self.__trip_repo.get_by_id(trip_id)
            if not trip_found:
                raise TripNotFoundError(trip_id)

            trip_found.confirm_guest(email_to_invite_id, fullname)

            await self.__trip_repo.save(trip_found)
