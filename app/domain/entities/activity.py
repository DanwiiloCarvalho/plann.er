from datetime import date, time
from uuid import UUID


class Activity:
    def __init__(
        self, id: UUID,
        title: str,
        date: date,
        time: time,
        trip_id: UUID
    ) -> None:
        self.__id = id
        self.__title = title
        self.__date = date
        self.__time = time
        self.__trip_id = trip_id

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str) -> None:
        self.__title = title

    @property
    def date(self) -> date:
        return self.__date

    @date.setter
    def date(self, date: date) -> None:
        self.__date = date

    @property
    def time(self) -> time:
        return self.__time

    @time.setter
    def time(self, time: time) -> None:
        self.__time = time

    @property
    def trip_id(self) -> UUID:
        return self.__trip_id
