from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.trip import Trip


class Link(Base):
    __tablename__ = 'links'

    link: Mapped[str] = mapped_column(String(400), nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('trips.id'), nullable=False)

    trip: Mapped['Trip'] = relationship(
        back_populates='links', lazy='select')
