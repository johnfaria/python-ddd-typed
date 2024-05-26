from dataclasses import dataclass
from enum import Enum
from typing import Optional, Self

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
    status: UserStatus

    def __init__(
        self, props: UserProps, status: UserStatus, id: Optional[str] = None
    ) -> None:
        self.id = id
        self.props = props
        self.status = status

    @classmethod
    def create(cls, props: UserProps) -> Self:
        return cls(props, status=UserStatus.ACTIVE)

    @classmethod
    def restore(cls, id: str, props: UserProps, status: UserStatus) -> Self:
        return cls(props, status, id)

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
