from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID, String, Boolean, DateTime, ForeignKey, func
from datetime import datetime
import uuid


class EmailToInvite(Base):
    __tablename__ = 'emails_to_invite'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    email: Mapped[str] = mapped_column(
        String(200), nullable=False, unique=True)
    fullname: Mapped[str] = mapped_column(String(200), nullable=True)
    presence: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False)
    trip_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('trips.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now())

    # trip: Mapped['Trip'] = relationship(
    #     back_populates='emails_to_invite', lazy='joined')
