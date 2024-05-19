from typing import Protocol


class Entity[T](Protocol):
    id: str

    def equals(self, other: T) -> bool:
        return self.id == other.id


class AggregateRoot[T](Entity[T]): ...
