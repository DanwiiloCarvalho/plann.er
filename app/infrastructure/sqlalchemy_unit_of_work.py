from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.ports.output_ports.unit_of_work import UnitOfWork


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db_session: AsyncSession) -> None:
        self.__db_session = db_session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.__db_session.rollback()
        else:
            await self.__db_session.commit()

    async def commit(self) -> None:
        await self.__db_session.commit()

    async def rollback(self) -> None:
        await self.__db_session.rollback()
