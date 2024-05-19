import uuid
from dataclasses import dataclass
from enum import Enum
from typing import Self

from src.core.domain.protocols.entity_protocol import Entity


@dataclass
class UserProps:
    name: str
    email: str
    password: str


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class User(Entity[UserProps]):
    status: UserStatus

    def __init__(
        self, props: UserProps, status: UserStatus, id: str | None = None
    ) -> None:
        self.id = id if id else str(uuid.uuid4())
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
