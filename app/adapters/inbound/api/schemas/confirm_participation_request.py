from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class ConfirmParticipationRequest(BaseSchema):
    fullname: str
