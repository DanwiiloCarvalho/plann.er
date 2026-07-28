import uuid
from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.inbound.api.deps import get_confirm_trip_use_case, get_create_trip_use_case, get_db
from app.adapters.inbound.api.schemas.confirm_participation_request import ConfirmParticipationRequest
from app.adapters.inbound.api.schemas.create_activity_request import CreateActivityRequest
from app.adapters.inbound.api.schemas.create_activity_response import CreateActivityResponse
from app.adapters.inbound.api.schemas.create_email_to_invite_request import CreateEmailToInviteRequest
from app.adapters.inbound.api.schemas.create_email_to_invite_response import CreateEmailToInviteResponse
from app.adapters.inbound.api.schemas.create_link_request import CreateLinkRequest
from app.adapters.inbound.api.schemas.create_link_response import CreateLinkResponse
from app.adapters.inbound.api.schemas.create_trip_request import CreateTripRequest
from app.adapters.inbound.api.schemas.create_trip_response import CreateTripResponse
from app.adapters.inbound.api.schemas.get_trip_response import GetTripResponse
from app.adapters.inbound.api.schemas.get_email_to_invite_response import GetEmailToInviteListResponse, GetEmailToInviteResponse
from app.adapters.inbound.api.schemas.get_activities_response import GetActivitiesListResponse, GetActivityResponse
from app.adapters.outbound.database.repositories.sqlalchemy_trip_repository import SqlAlchemyTripRepository
from app.application.dto.activity_dto import ActivityDTO
from app.application.dto.email_dto import EmailToInviteDTO
from app.application.dto.link_dto import LinkDTO
from app.application.dto.trip_dto import CreateTripDTO
from app.application.use_cases.confirm_participation_use_case import ConfirmParticipationUseCase
from app.application.use_cases.confirm_trip_use_case import ConfirmTripUseCase
from app.application.use_cases.create_activity_use_case import CreateActivityUseCase
from app.application.use_cases.create_email_to_invite_use_case import CreateEmailToInviteUseCase
from app.application.use_cases.create_trip_link_use_case import CreateTripLinkUseCase
from app.application.use_cases.create_trip_use_case import CreateTripUseCase
from app.application.use_cases.get_trip_by_id_use_case import GetTripByIdUseCase
from app.application.use_cases.get_emails_to_invite_use_case import GetEmailsToInviteUseCase
from app.application.use_cases.get_trip_activities_use_case import GetTripActivitiesUseCase
from app.domain.exceptions.activity_outside_trip_dates_error import ActivityOutsideTripDatesError
from app.domain.exceptions.email_to_invite_confirmed_error import EmailToInviteConfirmedError
from app.domain.exceptions.email_to_invite_not_found_error import EmailToInviteNotFoundError
from app.domain.exceptions.invalid_trip_dates_error import InvalidTripDatesError
from app.domain.exceptions.invalid_url_protocol_error import InvalidUrlProtocolError
from app.domain.exceptions.trip_not_found_error import TripNotFoundError
from app.domain.exceptions.trip_start_date_in_past_error import TripStartDateInPastError
from app.domain.exceptions.unconfirmed_trip_error import UnconfirmedTripError
from app.domain.ports.input_ports.confirm_trip_port import ConfirmTripPort
from app.domain.ports.input_ports.create_trip_port import CreateTripPort
from app.infrastructure.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


@router.post(
    '',
    description='Cria uma nova viagem',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTripResponse
)
async def create_trip(new_trip: CreateTripRequest, create_trip_use_case: CreateTripPort = Depends(get_create_trip_use_case)) -> CreateTripResponse:
    try:

        emails_list = [EmailToInviteDTO(email=email.email_to_invite)
                       for email in new_trip.emails_to_invite]

        new_trip_dto = CreateTripDTO(
            destination=new_trip.destination,
            start_date=new_trip.start_date,
            end_date=new_trip.end_date,
            owner_name=new_trip.owner_name,
            owner_email=str(new_trip.owner_email),
            emails_to_invite=emails_list
        )
        trip_created = await create_trip_use_case.execute(new_trip_dto)
        return CreateTripResponse.model_validate(trip_created)
    except (TripStartDateInPastError, InvalidTripDatesError) as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exception))


@router.get(
    '/{trip_id}',
    description='Recupera uma viagem',
    status_code=status.HTTP_200_OK,
    response_model=GetTripResponse
)
async def get_trip_by_id(trip_id: uuid.UUID, db_session: AsyncSession = Depends(get_db)) -> GetTripResponse:
    trip_repo = SqlAlchemyTripRepository(db_session)
    get_trip_by_id_use_case = GetTripByIdUseCase(trip_repo)
    trip_found = await get_trip_by_id_use_case.execute(trip_id)

    if not trip_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Trip not found.')
    return GetTripResponse.model_validate(trip_found)


@router.post(
    '/{trip_id}/confirm',
    description='Confirma uma viagem',
    status_code=status.HTTP_204_NO_CONTENT
)
async def confirm_trip(trip_id: uuid.UUID, confirm_trip_use_case: ConfirmTripPort = Depends(get_confirm_trip_use_case)) -> None:
    try:
        await confirm_trip_use_case.execute(trip_id)
    except TripNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))


@router.post(
    '/{trip_id}/links',
    description='Adiciona um link a uma viagem',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateLinkResponse
)
async def create_trip_link(trip_id: uuid.UUID, link: CreateLinkRequest, db_session: AsyncSession = Depends(get_db)) -> CreateLinkResponse:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        uow = SqlAlchemyUnitOfWork(db_session)
        create_trip_link_use_case = CreateTripLinkUseCase(trip_repo, uow)
        link_created = await create_trip_link_use_case.execute(trip_id, LinkDTO(link.link, link.title))
        return CreateLinkResponse.model_validate(link_created)
    except TripNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))
    except (UnconfirmedTripError, InvalidUrlProtocolError) as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exception))


@router.post(
    '/{trip_id}/activities',
    description='Adiciona uma atividade a uma viagem',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateActivityResponse
)
async def create_trip_activity(trip_id: uuid.UUID, activity: CreateActivityRequest, db_session: AsyncSession = Depends(get_db)) -> CreateActivityResponse:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        uow = SqlAlchemyUnitOfWork(db_session)
        create_trip_activity_use_case = CreateActivityUseCase(trip_repo, uow)
        activity_created = await create_trip_activity_use_case.execute(trip_id, ActivityDTO(activity.title, activity.date, activity.time))
        return CreateActivityResponse.model_validate(activity_created)
    except TripNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))
    except UnconfirmedTripError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exception))
    except ActivityOutsideTripDatesError as exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exception))


@router.post(
    '/{trip_id}/emails_to_invite',
    description='Adiciona um e-mail de convite a uma viagem',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateEmailToInviteResponse
)
async def create_email_to_invite(
    trip_id: uuid.UUID,
    email_to_invite: CreateEmailToInviteRequest,
    db_session: AsyncSession = Depends(get_db)
) -> CreateEmailToInviteResponse:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        uow = SqlAlchemyUnitOfWork(db_session)
        create_email_to_invite_use_case = CreateEmailToInviteUseCase(
            trip_repo, uow)
        email_created = await create_email_to_invite_use_case.execute(
            trip_id,
            EmailToInviteDTO(email=str(email_to_invite.email))
        )
        return CreateEmailToInviteResponse.model_validate(email_created)
    except TripNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))


@router.post(
    '/{trip_id}/emails_to_invite/{email_to_invite_id}/confirm',
    description='Confirma a presença do convidado em uma viagem',
    status_code=status.HTTP_204_NO_CONTENT
)
async def confirm_participation_in_the_trip(
    trip_id: uuid.UUID,
    email_to_invite_id: uuid.UUID,
    confirmation_data: ConfirmParticipationRequest,
    db_session: AsyncSession = Depends(get_db)
) -> None:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        uow = SqlAlchemyUnitOfWork(db_session)
        confirm_participation_use_case = ConfirmParticipationUseCase(
            trip_repo, uow)
        await confirm_participation_use_case.execute(trip_id, email_to_invite_id, confirmation_data.fullname)
    except (TripNotFoundError, EmailToInviteNotFoundError) as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))
    except EmailToInviteConfirmedError as exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exception))


@router.get(
    '/{trip_id}/emails_to_invite',
    description='Recupera os emails a serem convidados para uma viagem',
    status_code=status.HTTP_200_OK,
    response_model=GetEmailToInviteListResponse
)
async def get_emails_to_invite(trip_id: uuid.UUID, db_session: AsyncSession = Depends(get_db)) -> GetEmailToInviteListResponse:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        get_emails_to_invite_use_case = GetEmailsToInviteUseCase(trip_repo)
        emails_to_invite_dto = await get_emails_to_invite_use_case.execute(trip_id)
        emails_to_invite = [GetEmailToInviteResponse.model_validate(
            email_to_invite) for email_to_invite in emails_to_invite_dto]
        return GetEmailToInviteListResponse(emails_to_invite=emails_to_invite)
    except TripNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))


@router.get(
    '/{trip_id}/activities',
    description='Recupera atividades de uma viagem',
    status_code=status.HTTP_200_OK,
    response_model=GetActivitiesListResponse
)
async def get_trip_activities(trip_id: uuid.UUID, db_session: AsyncSession = Depends(get_db)) -> GetActivitiesListResponse:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        get_trip_activities_use_case = GetTripActivitiesUseCase(trip_repo)
        trip_activities_dto = await get_trip_activities_use_case.execute(trip_id)
        trip_activities = [GetActivityResponse.model_validate(
            activity) for activity in trip_activities_dto]
        return GetActivitiesListResponse(activities=trip_activities)
    except TripNotFoundError as exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))
