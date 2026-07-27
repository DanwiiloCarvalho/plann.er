from collections.abc import AsyncGenerator
from fastapi import BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.adapters.outbound.database.email.background_task_notification_sender import BackgroundTaskNotificationSender
from app.adapters.outbound.database.email.smtp_email_sender import SMTPEmailSender
from app.adapters.outbound.database.repositories.sqlalchemy_trip_repository import SqlAlchemyTripRepository
from app.application.use_cases.create_trip_use_case import CreateTripUseCase
from app.domain.ports.create_trip_port import CreateTripPort
from app.infrastructure.config import settings
from app.infrastructure.database import Session
from app.infrastructure.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session


def get_create_trip_use_case(background_tasks: BackgroundTasks, db_session: AsyncSession = Depends(get_db)) -> CreateTripPort:
    smtp_email_sender = SMTPEmailSender()
    notification_sender = BackgroundTaskNotificationSender(
        background_tasks, smtp_email_sender)
    email_message = f'Para confirmar a viagem, clique em: http://{settings.APP_HOST}:{settings.APP_PORT}/api/trips'
    trip_repo = SqlAlchemyTripRepository(db_session)
    uow = SqlAlchemyUnitOfWork(db_session)

    return CreateTripUseCase(
        trip_repo,
        uow,
        notification_sender,
        email_message
    )
