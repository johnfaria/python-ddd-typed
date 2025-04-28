from dataclasses import dataclass
from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class GetUserInput:
    user_id: str


@dataclass
class GetUserOutput:
    user_id: str
    name: str
    email: str


class GetUserUseCase(UseCaseProtocol[GetUserInput, GetUserOutput]):
    def __init__(self, user_repository: UserRepositoryProtocol) -> None:
        self.user_repository = user_repository

    async def handle(self, input: GetUserInput) -> GetUserOutput:
        user = await self.user_repository.find_by_id(input.user_id)
        if not user:
            raise ValueError("User not found")
        return GetUserOutput(
            user_id=user.id,
            name=user.props.name,
            email=user.props.email,
        )
