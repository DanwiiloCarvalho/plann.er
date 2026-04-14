from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, DateTime, String, ForeignKey, func
from datetime import datetime
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.trip import Trip


class Link(Base):
    __tablename__ = 'links'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    link: Mapped[str] = mapped_column(String(400), nullable=False)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('trips.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now())

    trip: Mapped['Trip'] = relationship(
        back_populates='links', lazy='joined')
