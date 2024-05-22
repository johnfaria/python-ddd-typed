import asyncio
from src.core.domain.protocols.entity_protocol import AggregateRoot
from src.core.domain.protocols.repository_protocol import Repository


class GenericRepositoryInMemory[T: AggregateRoot](Repository[T]):
    entities: list[T]

    def __init__(self):
        self.entities = []

    async def create(self, entity: T) -> None:
        self.entities.append(entity)

    async def find_by_id(self, entity_id: str) -> T | None:
        user = next(
            (entity for entity in self.entities if entity.id == entity_id), None
        )
        return user

    async def find_all(self) -> list[T]:
        return self.entities

    async def delete(self, entity_id: str) -> None:
        user = await self.find_by_id(entity_id)
        if not user:
            raise ValueError("Entity not found")
        self.entities.remove(user)

    async def update(self, entity: T) -> None:
        user = await self.find_by_id(entity.id)
        if not user:
            raise ValueError("Entity not found")
        self.entities.remove(user)
        self.entities.append(entity)

    async def bulk_create(self, entities: list[T]) -> None:
        await asyncio.gather(*(self.create(entity) for entity in entities))
