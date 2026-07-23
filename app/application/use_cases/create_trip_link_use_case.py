import uuid
from app.application.dto.link_dto import LinkDTO, LinkResponseDTO
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.trip_repository import TripRepository
from app.domain.ports.unit_of_work import UnitOfWork
from app.domain.entities.link import Link
from app.domain.value_objects.link import Link as LinkValueObject


class CreateTripLinkUseCase:
    def __init__(
        self,
        trip_repo: TripRepository,
        uow: UnitOfWork
    ) -> None:
        self.__trip_repo = trip_repo
        self.__uow = uow

    async def execute(self, trip_id: uuid.UUID, link: LinkDTO) -> LinkResponseDTO:
        async with self.__uow:
            trip_found = await self.__trip_repo.get_by_id(trip_id)
            if not trip_found:
                raise TripNotFoundError(trip_id)

            new_link = Link(
                id=uuid.uuid1(),
                link=LinkValueObject(link.link).address,
                title=link.title
            )

            trip_found.links = new_link
            await self.__trip_repo.save(trip_found)

            return LinkResponseDTO(
                id=new_link.id,
                link=new_link.link,
                title=new_link.title
            )
