from abc import ABC, abstractmethod

from app.application.dto.trip_dto import CreateTripDTO, CreateTripOutputDTO


class CreateTripPort(ABC):
    @abstractmethod
    async def execute(self, trip_dto: CreateTripDTO) -> CreateTripOutputDTO:
        pass
