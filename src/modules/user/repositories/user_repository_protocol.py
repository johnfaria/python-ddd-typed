from typing import Protocol, runtime_checkable

from core.domain.protocols.repository_protocol import Repository
from modules.user.domain.entities.user import User


@runtime_checkable
class UserRepositoryProtocol(Repository, Protocol):
    async def find_by_email(self, email: str) -> User | None: ...
