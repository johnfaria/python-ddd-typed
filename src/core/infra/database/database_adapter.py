from abc import abstractmethod
from typing import Any, Protocol


class DatabaseConnectionManager(Protocol):
    connection: Any

    @abstractmethod
    async def connect(self, db_name: str, document_models: list[Any]) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def is_connected(self) -> bool: ...


class DatabaseDocumentManager(Protocol):
    __documents: list[Any]

    @abstractmethod
    def add_document(self, document: Any) -> None: ...
