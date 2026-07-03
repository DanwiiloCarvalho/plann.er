from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from collections.abc import Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from app.adapters.outbound.database.mappers.email_to_invite_mapper import EmailToInviteMapper
from app.adapters.outbound.database.repositories.base_repository import BaseRepository
from app.adapters.outbound.database.models.email_to_invite import EmailToInvite as EmailToInviteModel
from app.domain.entities.email_to_invite import EmailToInvite as EmailToInviteDomain
from uuid import UUID


class EmailToInviteRepository(BaseRepository[EmailToInviteModel, EmailToInviteDomain]):
    def __init__(self, db_session: AsyncSession) -> None:
        super().__init__(db_session, EmailToInviteModel, EmailToInviteMapper)

    async def confirm_presence_by_id(self, email_to_invite_id: UUID) -> EmailToInviteDomain:
        query = select(self._model_cls).filter(
            self._model_cls.id == email_to_invite_id)
        result = await self._db_session.execute(query)
        email_to_invite_found: EmailToInviteModel | None = result.scalar_one_or_none()

        if not email_to_invite_found:
            raise ValueError(
                f'Email to invite with id {email_to_invite_id} not found')

        email_to_invite_found.presence = True
        return self._mapper.to_domain(email_to_invite_found)

        # query = select(EmailToInvite).filter(
        #     EmailToInvite.id == email_to_invite_id)
        # email_to_invite_found: EmailToInvite | None = (await self._db_session.execute(query)).scalar_one_or_none()

        # if not email_to_invite_found:
        #     return None

        # email_to_invite_found.presence = True
        # await self._db_session.commit()
        # return email_to_invite_found

    # async def add_emails_bulk(self, emails_to_invite: list[EmailToInvite]) -> list[EmailToInvite]:

    #     if not emails_to_invite:
    #         return []

    #     try:
    #         self._db_session.add_all(emails_to_invite)
    #         await self._db_session.commit()
    #         return emails_to_invite
    #     except IntegrityError as e:
    #         await self._db_session.rollback()
    #         raise e

    # async def find_emails_from_trip(self, trip_id: UUID) -> list[EmailToInvite]:
    #     try:
    #         query = select(EmailToInvite).filter(
    #             EmailToInvite.trip_id == trip_id)
    #         emails_found: Sequence[EmailToInvite] = (await self._db_session.execute(query)).scalars().all()
    #         return list(emails_found)
    #     except SQLAlchemyError as e:
    #         raise e
