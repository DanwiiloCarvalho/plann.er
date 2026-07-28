from abc import ABC, abstractmethod
import uuid


class ConfirmTripPort(ABC):
    @abstractmethod
    async def execute(self, trip_id: uuid.UUID) -> None:
        pass
