from uuid import UUID


class TripNotFoundError(Exception):
    def __init__(self, trip_id: UUID):
        self.trip_id = trip_id
