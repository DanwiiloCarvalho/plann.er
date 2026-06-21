from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UUID, DateTime, func
from datetime import datetime
import uuid


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now())
