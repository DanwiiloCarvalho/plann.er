from datetime import date
from pydantic import EmailStr

from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class EmailToInviteRequest(BaseSchema):
    fullname: str
    email_to_invite: EmailStr


class CreateTripRequest(BaseSchema):
    destination: str
    start_date: date
    end_date: date
    owner_name: str
    owner_email: EmailStr
    emails_to_invite: list[EmailToInviteRequest]
