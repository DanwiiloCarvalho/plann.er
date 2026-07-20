class TripStartDateInPastError(Exception):
    def __init__(self) -> None:
        super().__init__('The start date cannot be earlier than the current date.')
