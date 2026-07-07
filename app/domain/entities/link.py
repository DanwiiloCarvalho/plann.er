from uuid import UUID
from app.domain.value_objects.link import Link


class Link:
    def __init__(
        self,
        id: UUID,
        link: Link,
        title: str,
        trip_id: UUID = None
    ) -> None:
        self.__id = id
        self.__link = link
        self.__title = title
        self.__trip_id = trip_id

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def link(self) -> Link:
        return self.__link

    @link.setter
    def link(self, link: Link) -> None:
        self.__link = link

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = title

    @property
    def trip_id(self) -> UUID:
        return self.__trip_id

    @trip_id.setter
    def trip_id(self, trip_id: UUID) -> None:
        self.__trip_id = trip_id

    def __repr__(self) -> str:
        return self.link
