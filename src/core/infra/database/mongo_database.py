from typing import Any, Sequence
from core.infra.database.database_adapter import (
    DatabaseConnectionManager,
    DatabaseDocumentManager,
)
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, init_beanie


class MongoConnectionManager(DatabaseConnectionManager):
    def __init__(self, connection_string: str):
        self.connection: AsyncIOMotorClient[dict[str, Any]] = AsyncIOMotorClient[
            dict[str, Any]
        ](connection_string)

    async def connect(
        self, db_name: str, document_models: Sequence[type[Document]]
    ) -> None:
        await init_beanie(
            database=getattr(self.connection, db_name), document_models=document_models
        )

    async def disconnect(self):
        self.connection.close()

    async def is_connected(self) -> bool:
        try:
            await self.connection.admin.command("ping")
            return True
        except Exception:
            return False


class MongoDocumentManager[T](DatabaseDocumentManager[T]):
    def __init__(self):
        self._documents = []

    def add_document(self, document: T):
        self._documents.append(document)

    @property
    def documents(self):
        return self._documents
