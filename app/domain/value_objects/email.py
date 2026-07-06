from dataclasses import dataclass
import re

from app.domain.exceptions.invalid_email_error import InvalidEmailError


@dataclass(frozen=True)
class Email:
    email: str

    def __post_init__(self):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(pattern, self.email):
            raise InvalidEmailError(self.email)
