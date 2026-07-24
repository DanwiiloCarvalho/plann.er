from uuid import UUID


class EmailToInviteNotFoundError(Exception):
    def __init__(self, email_to_invite_id: UUID) -> None:
        self.email_to_invite_id = email_to_invite_id
        super().__init__(
            f'Email to invite with ID {email_to_invite_id} was not found.'
        )
