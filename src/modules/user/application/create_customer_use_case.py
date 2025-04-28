from dataclasses import dataclass

from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.domain.entities.user import CreateUserProps, User
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class CreateUserInput:
    name: str
    email: str
    password: str


@dataclass
class CreateUserOutput:
    id: str
    name: str
    email: str
    status: str


class CreateUserUseCase(UseCaseProtocol[CreateUserInput, CreateUserOutput]):
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def handle(self, input: CreateUserInput) -> CreateUserOutput:
        user = await self.user_repository.find_by_email(input.email)
        if user:
            raise ValueError("User already exists")
        user_id = self.user_repository.next_id()
        props = CreateUserProps(input.name, input.email, input.password)
        user = User.create(user_id, props)
        await self.user_repository.create(user)
        return CreateUserOutput(
            user.id,
            user.props.name,
            user.props.email,
            user.props.status.value,
        )
