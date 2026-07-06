class NetlocNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('Network location not found.')
