class InvalidTripDatesError(Exception):
    def __init__(self) -> None:
        super().__init__('The end date must be later than the start date.')
