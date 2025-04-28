from typing import Protocol

from core.domain.protocols.repository_protocol import Repository
from modules.user.domain.entities.user import User


class UserRepositoryProtocol(Repository[User], Protocol):
    async def find_by_email(self, email: str) -> User | None: ...
