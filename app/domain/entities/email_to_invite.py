from uuid import UUID


class EmailToInvite:
    def __init__(
        self,
        id: UUID,
        email: str,
        fullname: str,
        presence: bool,
        trip_id: UUID
    ) -> None:
        self.__id = id
        self.__email = email
        self.__fullname = fullname
        self.__presence = presence
        self.__trip_id = trip_id

    @property
    def id(self) -> UUID:
        return self.__id

    @id.setter
    def id(self, id: UUID) -> None:
        self.__id = id

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
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
