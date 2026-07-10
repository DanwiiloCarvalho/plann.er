from uuid import UUID

from app.domain.value_objects.email import Email


class EmailToInvite:
    def __init__(
        self,
        id: UUID,
        email: Email,
        fullname: str,
        trip_id: UUID | None = None,
        presence: bool = False
    ) -> None:
        self.__id = id
        self.__email = email
        self.__fullname = fullname
        self.__presence = presence
        self.__trip_id = trip_id

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def email(self) -> Email:
        return self.__email

    @email.setter
    def email(self, email: Email) -> None:
        self.__email = email

    @property
    def fullname(self) -> str:
        return self.__fullname

    @fullname.setter
    def fullname(self, fullname: str) -> None:
        self.__fullname = fullname

    @property
    def presence(self) -> bool:
        return self.__presence

    @presence.setter
    def presence(self, presence: bool) -> None:
        self.__presence = presence

    @property
    def trip_id(self) -> UUID:
        return self.__trip_id

    @trip_id.setter
    def trip_id(self, trip_id: UUID) -> None:
        self.__trip_id = trip_id

    def __repr__(self) -> str:
        return self.__email
