import uuid
from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class CreateLinkResponse(BaseSchema):
    id: uuid.UUID
    link: str
    title: str
