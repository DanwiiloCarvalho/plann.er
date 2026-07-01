from datetime import datetime
from uuid import UUID


class Link:
    def __init__(self, id: UUID, link: str, title: str, trip_id: UUID, created_at: datetime | None = None) -> None:
        self.__id = id
        self.__link = link
        self.__title = title
        self.__trip_id = trip_id
        self.__created_at = created_at

    @property
    def id(self) -> UUID:
        return self.__id

    @id.setter
    def id(self, id: UUID) -> None:
        self.__id = id

    @property
    def link(self) -> str:
        return self.__link

    @link.setter
    def link(self, link: str) -> None:
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

    @property
    def created_at(self) -> datetime | None:
        return self.__created_at

    def __repr__(self) -> str:
        return self.link
