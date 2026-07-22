from dataclasses import dataclass
import uuid


@dataclass
class EmailToInviteDTO:
    fullname: str
    email: str


@dataclass
class EmailToInviteResponseDTO:
    id: uuid.UUID
    fullname: str
    email: str
    presence: bool


@dataclass
class GetEmailToInviteDTO:
    fullname: str
    email: str
    presence: bool
