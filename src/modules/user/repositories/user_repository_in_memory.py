from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol

from src.core.infra.repositories.generic_repository_in_memory import (
    GenericRepositoryInMemory,
)
from src.modules.user.domain.user import User


class UserRepositoryInMemory(GenericRepositoryInMemory[User], UserRepositoryProtocol):
    def find_by_email(self, email: str) -> User | None:
        for user in self.entities:
            if user.props.email == email:
                return user
        return None
