from app.adapters.outbound.database.models.base import Base
from abc import ABC, abstractmethod


class IMapper[M: Base, D](ABC):

    @staticmethod
    @abstractmethod
    def to_domain(model: M) -> D:
        pass

    @staticmethod
    @abstractmethod
    def to_model(domain: D) -> M:
        pass
