from app.adapters.outbound.database.mappers.imapper import IMapper
from app.adapters.outbound.database.models.link import Link as LinkModel
from app.domain.entities.link import Link as LinkDomain


class LinkMapper(IMapper[LinkModel, LinkDomain]):
    @staticmethod
    def to_domain(model: LinkModel) -> LinkDomain:
        return LinkDomain(
            id=model.id,
            link=model.link,
            title=model.title,
            trip_id=model.trip_id
        )

    @staticmethod
    def to_model(domain: LinkDomain) -> LinkModel:
        return LinkModel(
            id=domain.id,
            link=domain.link,
            title=domain.title,
            trip_id=domain.trip_id
        )
