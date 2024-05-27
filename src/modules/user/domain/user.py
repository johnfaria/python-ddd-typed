from dataclasses import dataclass
from enum import Enum
from typing import Self

from core.domain.protocols.entity_protocol import AggregateRoot


@dataclass
class UserProps:
    name: str
    email: str
    password: str


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(AggregateRoot[UserProps]):
    __slots__ = ["id", "props", "status"]
    status: UserStatus

    def __init__(
        self, id: str, props: UserProps, status: UserStatus
    ) -> None:
        self.id = id
        self.props = props
        self.status = status

    @classmethod
    def create(cls, id: str, props: UserProps) -> Self:
        return cls(id, props, status=UserStatus.ACTIVE)

    @classmethod
    def restore(cls, id: str, props: UserProps, status: UserStatus) -> Self:
        return cls(id, props, status)

    def deactivate(self) -> None:
        if self.status == UserStatus.INACTIVE:
            raise ValueError("User is already inactive")
        self.status = UserStatus.INACTIVE

    def activate(self) -> None:
        if self.status == UserStatus.ACTIVE:
            raise ValueError("User is already active")
        self.status = UserStatus.ACTIVE

    def __repr__(self) -> str:
        return f"User(id={self.id}, status={self.status})"
