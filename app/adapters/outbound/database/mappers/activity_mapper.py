from app.adapters.outbound.database.mappers.imapper import IMapper
from app.adapters.outbound.database.models.activity import Activity as ActivityModel
from app.domain.entities.activity import Activity as ActivityDomain


class ActivityMapper(IMapper[ActivityModel, ActivityDomain]):
    @staticmethod
    def to_domain(model: ActivityModel) -> ActivityDomain:
        return ActivityDomain(
            id=model.id,
            title=model.title,
            date=model.date,
            time=model.time,
            trip_id=model.trip_id
        )

    @staticmethod
    def to_model(domain: ActivityDomain) -> ActivityModel:
        return ActivityModel(
            id=domain.id,
            title=domain.title,
            date=domain.date,
            time=domain.time,
            trip_id=domain.trip_id
        )
