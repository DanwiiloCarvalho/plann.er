from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.inbound.api.deps import get_db
from app.adapters.inbound.api.schemas.create_trip_request import CreateTripRequest
from app.adapters.inbound.api.schemas.create_trip_response import CreateTripResponse
from app.adapters.outbound.database.repositories.sqlalchemy_trip_repository import SqlAlchemyTripRepository
from app.application.dto.email_dto import EmailToInviteDTO
from app.application.dto.trip_dto import CreateTripDTO
from app.application.use_cases.create_trip_use_case import CreateTripUseCase
from app.domain.exceptions.invalid_trip_dates_error import InvalidTripDatesError
from app.domain.exceptions.trip_start_date_in_past_error import TripStartDateInPastError
from app.infrastructure.sqlalchemy_unit_of_work import SqlAlchemyUnitOfWork

router = APIRouter()


@router.post(
    '',
    description='Cria uma nova viagem',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTripResponse
)
async def create_trip(new_trip: CreateTripRequest, db_session: AsyncSession = Depends(get_db)) -> CreateTripResponse:
    try:
        trip_repo = SqlAlchemyTripRepository(db_session)
        uow = SqlAlchemyUnitOfWork(db_session)
        create_trip_use_case = CreateTripUseCase(trip_repo, uow)
        emails_list = [EmailToInviteDTO(
            email.fullname, email.email_to_invite) for email in new_trip.emails_to_invite]

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
