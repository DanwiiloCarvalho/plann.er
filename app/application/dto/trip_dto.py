from dataclasses import dataclass
from datetime import date
import uuid

from app.application.dto.email_dto import EmailToInviteDTO


@dataclass
class CreateTripDTO:
    destination: str
    start_date: date
    end_date: date
    owner_name: str
    owner_email: str
    emails_to_invite: list[EmailToInviteDTO]


@dataclass
class CreateTripOutputDTO:
    id: uuid.UUID
    destination: str
    start_date: date
    end_date: date
    owner_name: str
    owner_email: str
