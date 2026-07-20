from dataclasses import dataclass


@dataclass
class EmailToInviteDTO:
    fullname: str
    email: str
