from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.trip import Trip


class TripRepository(ABC):
    @abstractmethod
    def get_by_id(self, trip_id: UUID) -> Trip | None:
        pass

    @abstractmethod
    def save(self, trip: Trip) -> None:
        pass

    @abstractmethod
    def delete(self, trip: Trip) -> None:
        pass
