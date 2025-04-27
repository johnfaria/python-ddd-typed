from dataclasses import dataclass
from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class ListUsersOutput:
    id: str
    email: str
    name: str
    status: str


class ListUsersUseCase(UseCaseProtocol[None, None]):
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def handle(self, input: None = None):
        users = await self.user_repository.find_all()
        return [
            ListUsersOutput(
                id=str(user.id),
                email=user.props.email,
                name=user.props.name,
                status=user.props.status.value,
            )
            for user in users
        ]
