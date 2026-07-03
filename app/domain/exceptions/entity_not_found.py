from uuid import UUID


class EntityNotFoundError(Exception):
    def __init__(self, entity_id: UUID) -> None:
        self.entity_id = entity_id
