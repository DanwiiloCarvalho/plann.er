from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, Date, Boolean, DateTime, func
from datetime import date, datetime
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.email_to_invite import EmailToInvite
    from app.models.link import Link


class Trip(Base):
    __tablename__ = 'trips'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    destination: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_email: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now())

    activities: Mapped[list['Activity']] = relationship(
        back_populates='trip', lazy='joined', cascade='all, delete-orphan')
    links: Mapped[list['Link']] = relationship(
        back_populates='trip', lazy='joined', cascade='all, delete-orphan')
    emails_to_invite: Mapped[list['EmailToInvite']] = relationship(
        back_populates='trip', lazy='joined', cascade='all, delete-orphan')
