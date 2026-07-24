from dataclasses import dataclass
import uuid


@dataclass
class EmailToInviteDTO:
    email: str


@dataclass
class EmailToInviteResponseDTO:
    id: uuid.UUID
    email: str
    presence: bool


@dataclass
class EmailToInviteListResponseDTO:
    id: uuid.UUID
    fullname: str
    email: str
    presence: bool


@dataclass
class GetEmailToInviteDTO:
    fullname: str
    email: str
    presence: bool
