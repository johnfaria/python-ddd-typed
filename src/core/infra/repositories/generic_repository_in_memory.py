from src.core.domain.protocols.entity_protocol import Entity
from src.core.domain.protocols.repository_protocol import Repository


class GenericRepositoryInMemory[T: Entity](Repository[T]):
    entities: list[T]

    def __init__(self):
        self.entities = []

    def create(self, entity: T) -> None:
        self.entities.append(entity)

    def find_by_id(self, entity_id: str) -> T | None:
        user = next(
            (entity for entity in self.entities if entity.id == entity_id), None
        )
        return user

    def find_all(self) -> list[T]:
        return self.entities

    def delete(self, entity_id: str) -> None:
        user = self.find_by_id(entity_id)
        if not user:
            raise ValueError("Entity not found")
        self.entities.remove(user)

    def update(self, entity: T) -> None:
        user = self.find_by_id(entity.id)
        self.entities.remove(user)
        self.entities.append(entity)
