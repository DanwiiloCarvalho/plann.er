from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Time, ForeignKey
from datetime import date, time
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.trip import Trip


class Activity(Base):
    __tablename__ = 'activities'

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('trips.id'), nullable=False)

    trip: Mapped['Trip'] = relationship(
        back_populates='activities', lazy='joined')
