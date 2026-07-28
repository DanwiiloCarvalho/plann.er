import uuid
from app.application.dto.activity_dto import ActivityDTO
from app.application.dto.email_dto import EmailToInviteResponseDTO
from app.application.dto.email_dto import EmailToInviteListResponseDTO
from app.application.dto.link_dto import LinkDTO
from app.application.dto.trip_dto import GetTripDTO
from app.domain.ports.output_ports.trip_repository import TripRepository
from app.domain.ports.output_ports.unit_of_work import UnitOfWork
from app.domain.exceptions.trip_not_found_error import TripNotFoundError


class GetEmailsToInviteUseCase:
    def __init__(
        self,
        trip_repo: TripRepository
    ) -> None:
        self.__trip_repo = trip_repo

    async def execute(self, trip_id: uuid.UUID) -> list[EmailToInviteListResponseDTO]:
        trip_found = await self.__trip_repo.get_by_id(trip_id)
        if not trip_found:
            raise TripNotFoundError(trip_id)

        emails_to_invite = [EmailToInviteListResponseDTO(
            email_to_invite.id, email_to_invite.fullname, email_to_invite.email.email, email_to_invite.presence) for email_to_invite in trip_found.emails_to_invite]

        return emails_to_invite
