from dataclasses import dataclass
from enum import Enum
from typing import Self

from core.domain.protocols.entity_protocol import AggregateRoot
from modules.user.domain.value_objects.password_vo import Password, PasswordProps


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class UserProps:
    name: str
    email: str
    status: UserStatus
    password: Password


@dataclass
class CreateUserProps:
    name: str
    email: str
    password: str


@dataclass
class RestoreUserProps:
    name: str
    email: str
    hashed_password: str
    salt: str
    status: str


class User(AggregateRoot[UserProps]):
    __slots__ = ["id", "props"]

    def __init__(self, id: str, props: UserProps) -> None:
        self.id = id
        self.props = props

    @classmethod
    def create(cls, id: str, props: CreateUserProps) -> Self:
        user_props = UserProps(
            name=props.name,
            email=props.email,
            password=Password.create(props.password),
            status=UserStatus.ACTIVE,
        )
        return cls(id, user_props)

    @classmethod
    def restore(cls, id: str, props: RestoreUserProps) -> Self:
        pw_props = PasswordProps(props.hashed_password, props.salt)
        user_props = UserProps(
            name=props.name,
            email=props.email,
            password=Password(pw_props),
            status=UserStatus(props.status),
        )
        return cls(id, user_props)

    def deactivate(self) -> None:
        if self.props.status == UserStatus.INACTIVE:
            raise ValueError("User is already inactive")
        self.props.status = UserStatus.INACTIVE

    def activate(self) -> None:
        if self.props.status == UserStatus.ACTIVE:
            raise ValueError("User is already active")
        self.props.status = UserStatus.ACTIVE

    def is_active(self) -> bool:
        return self.props.status == UserStatus.ACTIVE

    def verify_password(self, password: str) -> bool:
        return self.props.password.verify(password)

    def __repr__(self) -> str:
        return f"User(id={self.id}, status={self.props.status})"
