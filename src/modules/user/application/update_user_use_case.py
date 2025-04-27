from dataclasses import dataclass

from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class UpdateUserInput:
    id: str
    name: str
    email: str


@dataclass
class UpdateUserOutput:
    id: str
    name: str
    email: str


class UpdateUserUseCase(UseCaseProtocol[UpdateUserInput, None]):
    def __init__(
        self,
        user_repository: UserRepositoryProtocol,
    ):
        self.user_repository = user_repository

    async def handle(self, input: UpdateUserInput):
        user = await self.user_repository.find_by_id(input.id)
        if not user:
            raise ValueError("User not found")
        user.props.name = input.name
        user.props.email = input.email
        await self.user_repository.update(user)
        return UpdateUserOutput(
            id=user.id,
            name=user.props.name,
            email=user.props.email,
        )
