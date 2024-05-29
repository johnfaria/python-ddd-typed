from dataclasses import dataclass

from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.infra.jwt.jwt_service import require_auth_jwt
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class UpdateUserInput:
    token: str
    id: str
    name: str
    email: str
    password: str


class UpdateUserUseCase(UseCaseProtocol[UpdateUserInput, None]):
    def __init__(
        self,
        user_repository: UserRepositoryProtocol,
    ):
        self.user_repository = user_repository

    @require_auth_jwt
    async def handle(self, input: UpdateUserInput):
        user = await self.user_repository.find_by_id(input.id)
        if not user:
            raise ValueError("User not found")
        user.props.name = input.name
        user.props.email = input.email
        await self.user_repository.update(user)
