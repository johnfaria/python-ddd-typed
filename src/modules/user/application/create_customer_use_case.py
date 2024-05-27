from dataclasses import dataclass
from typing import cast

from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.domain.user import User, UserProps
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class CreateCustomerInput:
    name: str
    email: str
    password: str


@dataclass
class CreateCustomerOutput:
    id: str
    name: str
    email: str
    status: str


class CreateCustomerUseCase(UseCaseProtocol[CreateCustomerInput, CreateCustomerOutput]):
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def handle(self, input: CreateCustomerInput) -> CreateCustomerOutput:
        user = await self.user_repository.find_by_email(input.email)
        if user:
            raise ValueError("User already exists")
        user_id = self.user_repository.next_id()
        props = UserProps(input.name, input.email, input.password)
        user = User.create(user_id, props)
        await self.user_repository.create(user)
        return CreateCustomerOutput(
            cast(str, user.id), user.props.name, user.props.email, user.status.value
        )
