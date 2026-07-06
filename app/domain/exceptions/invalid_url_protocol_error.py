class InvalidUrlProtocolError(Exception):
    def __init__(self) -> None:
        super().__init__(f'Invalid URL Protocol.')
