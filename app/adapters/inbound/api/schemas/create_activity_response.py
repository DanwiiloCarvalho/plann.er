import uuid
from app.adapters.inbound.api.schemas.base_schema import BaseSchema
from datetime import date, time


class CreateActivityResponse(BaseSchema):
    id: uuid.UUID
    title: str
    date: date
    time: time
