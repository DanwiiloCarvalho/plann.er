class UnconfirmedTripError(Exception):
    def __init__(self) -> None:
        super().__init__('Trip not confirmed.')
