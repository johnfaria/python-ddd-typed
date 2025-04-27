from core.infra.config.config_pydantic import get_settings
from core.infra.database.mongo_database import (
    MongoConnectionManager,
    MongoDocumentManager,
)
from core.infra.schemas.user_schema import UserDocument


# Global instances
settings = get_settings()
document_manager = MongoDocumentManager()
document_manager.add_document(UserDocument)
connection_manager = MongoConnectionManager(settings.database_url)


async def initialize_database():
    """Initializes the database connection."""
    await connection_manager.connect(settings.database_name, document_manager.documents)


async def close_database():
    """Closes the database connection."""
    await connection_manager.disconnect()
