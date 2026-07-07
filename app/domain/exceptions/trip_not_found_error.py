from uuid import UUID


class TripNotFoundError(Exception):
    def __init__(self, trip_id: UUID) -> None:
        self.trip_id = trip_id
        super().__init__(f'Trip with ID {trip_id} was not found.')
