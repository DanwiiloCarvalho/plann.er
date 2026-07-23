from pydantic import EmailStr

from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class CreateEmailToInviteRequest(BaseSchema):
    email: EmailStr
