import uuid
from datetime import date, time
from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class GetActivityResponse(BaseSchema):
    id: uuid.UUID
    title: str
    date: date
    time: time


class GetActivitiesListResponse(BaseSchema):
    activities: list[GetActivityResponse]
