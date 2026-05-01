from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import Base
from sqlalchemy.exc import SQLAlchemyError
from collections.abc import Sequence
from typing import Any
import uuid


class BaseRepository[T: Base]:
    def __init__(self, db_session: AsyncSession, model: type[T]) -> None:
        self._db_session = db_session
        self._model = model

    async def create(self, obj_in: T) -> T:
        try:
            self._db_session.add(obj_in)
            await self._db_session.commit()
            return obj_in
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise e

    async def get_by_id(self, obj_id: uuid.UUID) -> T | None:
        try:
            query = select(self._model).filter(self._model.id == obj_id)
            result = await self._db_session.execute(query)
            obj_found: T | None = result.unique().scalar_one_or_none()
            return obj_found
        except SQLAlchemyError as e:
            raise e

    async def list_all(self) -> list[T]:
        try:
            query = select(self._model)
            result = await self._db_session.execute(query)
            obj_sequence: Sequence[T] = result.unique().scalars().all()
            return list(obj_sequence)
        except SQLAlchemyError as e:
            raise e

    async def delete_by_id(self, obj_id: uuid.UUID) -> bool:
        try:
            query = select(self._model).filter(self._model.id == obj_id)
            result = await self._db_session.execute(query)
            obj_found: T | None = result.unique().scalar_one_or_none()

            if not obj_found:
                return False

            await self._db_session.delete(obj_found)
            await self._db_session.commit()
            return True
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise e

    async def update(self, obj_id: uuid.UUID, obj_in: dict[str, Any]) -> T | None:
        try:
            query = select(self._model).filter(self._model.id == obj_id)
            result = await self._db_session.execute(query)
            obj_found: T | None = result.unique().scalar_one_or_none()

            if not obj_found:
                return None

            for key, value in obj_in.items():
                setattr(obj_found, key, value)

            await self._db_session.commit()
            await self._db_session.refresh(obj_found)
            return obj_found
        except SQLAlchemyError as e:
            await self._db_session.rollback()
            raise e
