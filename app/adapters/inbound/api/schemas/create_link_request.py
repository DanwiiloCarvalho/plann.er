from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class CreateLinkRequest(BaseSchema):
    link: str
    title: str
