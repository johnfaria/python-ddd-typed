from typing import Optional, Protocol, Self


class Entity[T](Protocol):
    # TODO: Add __slots__ = ["id"] when Python 3.10 is released
    # TODO: Verify if the type of id should be Optional[str] or str | None
    id: Optional[str]

    def equals(self, other: Self) -> bool:
        return self.id == other.id

    def set_id(self, id: str) -> None:
        self.id = id


class AggregateRoot[T](Entity[T]): ...
