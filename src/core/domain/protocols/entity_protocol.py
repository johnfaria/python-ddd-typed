from typing import Protocol, Self


class Entity[T](Protocol):
    __slots__ = ["id"]
    id: str

    def equals(self, other: Self) -> bool:
        return self.id == other.id


class AggregateRoot[T](Entity[T]):
    __slots__ = ["id"]
