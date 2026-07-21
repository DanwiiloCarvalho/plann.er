from dataclasses import dataclass


@dataclass
class EmailToInviteDTO:
    fullname: str
    email: str


@dataclass
class GetEmailToInviteDTO:
    fullname: str
    email: str
    presence: bool
