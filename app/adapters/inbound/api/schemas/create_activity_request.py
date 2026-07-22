from app.adapters.inbound.api.schemas.base_schema import BaseSchema
from datetime import date, time


class CreateActivityRequest(BaseSchema):
    title: str
    date: date
    time: time
