from datetime import date, time
import uuid

from pydantic import EmailStr
from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class GetEmailToInviteListResponse(BaseSchema):
    id: uuid.UUID
    fullname: str | None
    email: EmailStr
    presence: bool
