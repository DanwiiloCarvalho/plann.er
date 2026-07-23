from datetime import date, time
import uuid

from pydantic import EmailStr
from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class GetEmailToInvite(BaseSchema):
    fullname: str | None
    email: EmailStr
    presence: bool


class GetLink(BaseSchema):
    link: str
    title: str


class GetActivity(BaseSchema):
    title: str
    date: date
    time: time


class GetTripResponse(BaseSchema):
    id: uuid.UUID
    destination: str
    start_date: date
    end_date: date
    owner_name: str
    owner_email: EmailStr
    emails_to_invite: list[GetEmailToInvite]
    links: list[GetLink]
    activities: list[GetActivity]
