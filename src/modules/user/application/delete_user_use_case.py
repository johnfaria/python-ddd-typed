from dataclasses import dataclass

from core.application.protocols.use_case_protocol import UseCaseProtocol

from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class DeleteUserInput:
    user_id: str


class DeleteUserUseCase(UseCaseProtocol[DeleteUserInput, None]):
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def handle(self, input: DeleteUserInput) -> None:
        user = await self.user_repository.find_by_id(input.user_id)
        if not user:
            raise ValueError("User not found")
        await self.user_repository.delete(user.id)
