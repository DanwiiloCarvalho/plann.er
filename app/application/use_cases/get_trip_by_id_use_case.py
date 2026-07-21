import uuid
from app.application.dto.email_dto import GetEmailToInviteDTO
from app.application.dto.link_dto import LinkDTO
from app.application.dto.trip_dto import GetTripDTO
from app.domain.ports.trip_repository import TripRepository
from app.domain.ports.unit_of_work import UnitOfWork


class GetTripByIdUseCase:
    def __init__(
        self,
        trip_repo: TripRepository
    ) -> None:
        self.__trip_repo = trip_repo

    async def execute(self, trip_id: uuid.UUID) -> GetTripDTO | None:
        trip_found = await self.__trip_repo.get_by_id(trip_id)
        if trip_found:
            emails_to_invite = [GetEmailToInviteDTO(
                email_to_invite.fullname, email_to_invite.email.email, email_to_invite.presence) for email_to_invite in trip_found.emails_to_invite]

            links = [LinkDTO(link.link, link.title)
                     for link in trip_found.links]

            trip_found = GetTripDTO(
                id=trip_found.id,
                destination=trip_found.destination,
                start_date=trip_found.start_date,
                end_date=trip_found.end_date,
                owner_name=trip_found.owner_name,
                owner_email=trip_found.owner_email.email,
                emails_to_invite=emails_to_invite,
                links=links
            )

        return trip_found
