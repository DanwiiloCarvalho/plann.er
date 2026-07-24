class EmailToInviteConfirmedError(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(
            f'The participant registered with the e-mail {email} has already been confirmed.')
