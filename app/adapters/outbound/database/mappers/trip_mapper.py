from app.adapters.outbound.database.mappers.activity_mapper import ActivityMapper
from app.adapters.outbound.database.mappers.email_to_invite_mapper import EmailToInviteMapper
from app.adapters.outbound.database.mappers.imapper import IMapper
from app.adapters.outbound.database.mappers.link_mapper import LinkMapper
from app.adapters.outbound.database.models.trip import Trip as TripModel
from app.domain.entities.trip import Trip as TripDomain
from app.domain.value_objects.email import Email


class TripMapper(IMapper[TripModel, TripDomain]):
    @staticmethod
    def to_domain(model: TripModel) -> TripDomain:
        return TripDomain(
            id=model.id,
            destination=model.destination,
            start_date=model.start_date,
            end_date=model.end_date,
            owner_name=model.owner_name,
            owner_email=Email(model.owner_email),
            status=model.status,
            activities=[ActivityMapper.to_domain(
                activity) for activity in model.activities],
            links=[LinkMapper.to_domain(link) for link in model.links],
            emails_to_invite=[EmailToInviteMapper.to_domain(
                email) for email in model.emails_to_invite]
        )

    @staticmethod
    def to_model(domain: TripDomain) -> TripModel:
        return TripModel(
            id=domain.id,
            destination=domain.destination,
            start_date=domain.start_date,
            end_date=domain.end_date,
            owner_name=domain.owner_name,
            owner_email=domain.owner_email.email,
            status=domain.status,
            activities=[ActivityMapper.to_model(
                activity) for activity in domain.activities],  # Faltando funcionar
            links=[LinkMapper.to_model(link)
                   for link in domain.links],  # Já funciona
            emails_to_invite=[EmailToInviteMapper.to_model(  # Faltando funcionar
                email) for email in domain.emails_to_invite]
        )
