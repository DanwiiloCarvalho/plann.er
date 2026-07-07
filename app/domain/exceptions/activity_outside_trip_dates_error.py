from datetime import date


class ActivityOutsideTripDatesError(Exception):
    def __init__(self) -> None:
        super().__init__('Activity date must be within the trip dates.')
