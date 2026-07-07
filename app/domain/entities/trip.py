from datetime import date
from uuid import UUID
from app.domain.entities.activity import Activity
from app.domain.entities.link import Link
from app.domain.entities.email_to_invite import EmailToInvite
from app.domain.exceptions.activity_outside_trip_dates_error import ActivityOutsideTripDatesError
from app.domain.exceptions.unconfirmed_trip_error import UnconfirmedTripError
from app.domain.value_objects.email import Email


class Trip:
    def __init__(
        self,
        id: UUID,
        destination: str,
        start_date: date,
        end_date: date,
        owner_name: str,
        owner_email: Email,
        status: bool = False,
        activities: list[Activity] = [],
        links: list[Link] = [],
        emails_to_invite: list[EmailToInvite] = []
    ) -> None:
        self.__id = id
        self.__destination = destination
        self.__start_date = start_date
        self.__end_date = end_date
        self.__owner_name = owner_name
        self.__owner_email = owner_email
        self.__status = status
        self.__activities = activities
        self.__links = links
        self.__emails_to_invite = emails_to_invite

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def destination(self) -> str:
        return self.__destination

    @destination.setter
    def destination(self, destination: str) -> None:
        self.__destination = destination

    @property
    def start_date(self) -> date:
        return self.__start_date

    @start_date.setter
    def start_date(self, start_date: date) -> None:
        self.__start_date = start_date

    @property
    def end_date(self) -> date:
        return self.__end_date

    @end_date.setter
    def end_date(self, end_date: date) -> None:
        self.__end_date = end_date

    @property
    def owner_name(self) -> str:
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, owner_name: str) -> None:
        self.__owner_name = owner_name

    @property
    def owner_email(self) -> Email:
        return self.__owner_email

    @owner_email.setter
    def owner_email(self, owner_email: Email) -> None:
        self.__owner_email = owner_email

    @property
    def status(self) -> bool:
        return self.__status

    @status.setter
    def status(self, status: bool) -> None:
        self.__status = status

    @property
    def activities(self) -> list[Activity]:
        return self.__activities

    @activities.setter
    def activities(self, activity: Activity) -> None:
        if not self.__status:
            raise UnconfirmedTripError
        if not (self.__start_date <= activity.date <= self.__end_date):
            raise ActivityOutsideTripDatesError
        self.__activities.append(activity)

    @property
    def links(self) -> list[Link]:
        return self.__links

    @links.setter
    def links(self, link: Link) -> None:
        if not self.__status:
            raise UnconfirmedTripError
        self.__links.append(link)

    @property
    def emails_to_invite(self) -> list[EmailToInvite]:
        return self.__emails_to_invite

    @emails_to_invite.setter
    def emails_to_invite(self, email_to_invite: EmailToInvite) -> None:
        self.__emails_to_invite.append(email_to_invite)
