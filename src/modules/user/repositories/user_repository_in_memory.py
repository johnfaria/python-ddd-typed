from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol

from core.infra.repositories.generic_repository_in_memory import (
    GenericRepositoryInMemory,
)
from modules.user.domain.entities.user import User


class UserRepositoryInMemory(GenericRepositoryInMemory[User], UserRepositoryProtocol):
    async def find_by_email(self, email: str) -> User | None:
        for user in self.entities:
            if user.props.email == email:
                return user
        return None
