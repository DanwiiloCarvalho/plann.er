from app.adapters.outbound.database.mappers.imapper import IMapper
from app.adapters.outbound.database.models.email_to_invite import EmailToInvite as EmailToInviteModel
from app.domain.entities.email_to_invite import EmailToInvite as EmailToInviteDomain


class EmailToInviteMapper(IMapper[EmailToInviteModel, EmailToInviteDomain]):
    @staticmethod
    def to_domain(model: EmailToInviteModel) -> EmailToInviteDomain:
        return EmailToInviteDomain(
            id=model.id,
            email=model.email,
            fullname=model.fullname,
            presence=model.presence,
            trip_id=model.trip_id
        )

    @staticmethod
    def to_model(domain: EmailToInviteDomain) -> EmailToInviteModel:
        return EmailToInviteModel(
            id=domain.id,
            email=domain.email,
            fullname=domain.fullname,
            presence=domain.presence,
            trip_id=domain.trip_id
        )
