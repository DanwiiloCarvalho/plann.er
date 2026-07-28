import uuid

from app.application.dto.email_dto import EmailToInviteDTO, EmailToInviteResponseDTO
from app.domain.entities.email_to_invite import EmailToInvite
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.output_ports.trip_repository import TripRepository
from app.domain.ports.output_ports.unit_of_work import UnitOfWork
from app.domain.value_objects.email import Email


class CreateEmailToInviteUseCase:
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
        email_to_invite: EmailToInviteDTO
    ) -> EmailToInviteResponseDTO:
        async with self.__uow:
            trip_found = await self.__trip_repo.get_by_id(trip_id)
            if not trip_found:
                raise TripNotFoundError(trip_id)

            new_email_to_invite = EmailToInvite(
                id=uuid.uuid1(),
                email=Email(email_to_invite.email)
            )

            trip_found.emails_to_invite = new_email_to_invite
            await self.__trip_repo.save(trip_found)

            return EmailToInviteResponseDTO(
                id=new_email_to_invite.id,
                email=new_email_to_invite.email.email,
                presence=new_email_to_invite.presence
            )
