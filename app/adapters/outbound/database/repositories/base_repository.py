from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.adapters.outbound.database.mappers.imapper import IMapper
from app.adapters.outbound.database.models.base import Base
from collections.abc import Sequence
from abc import ABC
import uuid

from app.domain.exceptions.entity_not_found import EntityNotFoundError


class BaseRepository[OrmModel: Base, DomainEntity](ABC):
    def __init__(
        self,
        db_session: AsyncSession,
        model_cls: type[OrmModel],
        mapper: type[IMapper[OrmModel, DomainEntity]]
    ) -> None:
        self._db_session = db_session
        self._model_cls = model_cls
        self._mapper = mapper

    async def create(self, obj_in: DomainEntity) -> DomainEntity:
        self._db_session.add(self._mapper.to_model(obj_in))
        await self._db_session.flush()
        return obj_in

    async def get_by_id(self, obj_id: uuid.UUID) -> DomainEntity | None:
        query = select(self._model_cls).filter(self._model_cls.id == obj_id)
        result = await self._db_session.execute(query)
        obj_found: OrmModel | None = result.scalar_one_or_none()

        return self._mapper.to_domain(obj_found) if obj_found else None

    async def list_all(self) -> list[DomainEntity]:
        query = select(self._model_cls)
        result = await self._db_session.execute(query)
        obj_sequence: Sequence[OrmModel] = result.scalars().all()
        obj_list = [self._mapper.to_domain(obj) for obj in list(obj_sequence)]
        return obj_list

    async def delete_by_id(self, obj_id: uuid.UUID) -> None:
        query = select(self._model_cls).filter(self._model_cls.id == obj_id)
        result = await self._db_session.execute(query)
        obj_found: OrmModel | None = result.scalar_one_or_none()

        if not obj_found:
            raise EntityNotFoundError(obj_id)

        await self._db_session.delete(obj_found)

    async def update(self, domain_entity: DomainEntity) -> DomainEntity:
        orm_model = self._mapper.to_model(domain_entity)
        query = select(self._model_cls).filter(
            self._model_cls.id == domain_entity.id)
        result = await self._db_session.execute(query)
        obj_found: OrmModel | None = result.scalar_one_or_none()

        if not obj_found:
            raise EntityNotFoundError(orm_model.id)

        for column in self._model_cls.__table__.columns:
            if column.name not in 'created_at, updated_at':
                setattr(obj_found, column.name,
                        getattr(orm_model, column.name))

        await self._db_session.refresh(obj_found)
        return self._mapper.to_domain(obj_found)
