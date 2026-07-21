import uuid
from app.application.dto.trip_dto import CreateTripDTO, CreateTripOutputDTO
from app.domain.entities.email_to_invite import EmailToInvite
from app.domain.entities.trip import Trip
from app.domain.ports.trip_repository import TripRepository
from app.domain.ports.unit_of_work import UnitOfWork
from app.domain.value_objects.email import Email


class CreateTripUseCase:
    def __init__(
        self,
        trip_repo: TripRepository,
        uow: UnitOfWork
    ) -> None:
        self.__trip_repo = trip_repo
        self.__uow = uow

    async def execute(self, trip_dto: CreateTripDTO) -> CreateTripOutputDTO:
        async with self.__uow:
            emails_to_invite = [EmailToInvite(id=uuid.uuid1(), email=Email(
                email_dto.email), fullname=email_dto.fullname) for email_dto in trip_dto.emails_to_invite]
            trip = Trip(
                id=uuid.uuid1(),
                destination=trip_dto.destination,
                start_date=trip_dto.start_date,
                end_date=trip_dto.end_date,
                owner_name=trip_dto.owner_name,
                owner_email=Email(trip_dto.owner_email),
                emails_to_invite=emails_to_invite
            )

            await self.__trip_repo.save(trip)
            return CreateTripOutputDTO(
                id=trip.id,
                destination=trip.destination,
                start_date=trip.start_date,
                end_date=trip.end_date,
                owner_name=trip.owner_name,
                owner_email=trip.owner_email.email
            )
