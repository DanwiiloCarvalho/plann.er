from datetime import date
from uuid import UUID
from app.adapters.inbound.api.schemas.base_schema import BaseSchema


class CreateTripResponse(BaseSchema):
    id: UUID
    destination: str
    start_date: date
    end_date: date
    owner_name: str
    owner_email: str
