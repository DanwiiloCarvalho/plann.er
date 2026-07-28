import uuid
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.ports.output_ports.notification_sender import NotificationSender
from app.domain.ports.output_ports.trip_repository import TripRepository
from app.domain.ports.output_ports.unit_of_work import UnitOfWork


class ConfirmTripUseCase:
    def __init__(
        self,
        trip_repo: TripRepository,
        uow: UnitOfWork,
        notification_sender: NotificationSender,
        email_message: str
    ) -> None:
        self.__trip_repo = trip_repo
        self.__uow = uow
        self.__notification_sender = notification_sender
        self.__email_message = email_message

    async def execute(self, trip_id: uuid.UUID) -> None:
        async with self.__uow:
            trip_found = await self.__trip_repo.get_by_id(trip_id)
            if not trip_found:
                raise TripNotFoundError(trip_id)
            trip_found.status = True
            await self.__trip_repo.save(trip_found)

            # emails_list = [
            #     email_to_invite.email.email for email_to_invite in trip_found.emails_to_invite]

            # self.__notification_sender.send_notification(
            #     emails_list, self.__email_message + f'/{trip_id}/emails_to_invite/{}/confirm')

            for email_to_invite in trip_found.emails_to_invite:
                self.__notification_sender.send_notification(
                    [email_to_invite.email.email], self.__email_message + f'/{trip_id}/emails_to_invite/{email_to_invite.id}/confirm')
