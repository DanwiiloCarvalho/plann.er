class InvalidEmailError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f'The email address {email} is invalid.')
