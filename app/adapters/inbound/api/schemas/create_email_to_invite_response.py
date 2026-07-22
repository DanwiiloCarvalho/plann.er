import uuid

from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class CreateEmailToInviteResponse(BaseSchema):
    id: uuid.UUID
    fullname: str
    email: str
    presence: bool
