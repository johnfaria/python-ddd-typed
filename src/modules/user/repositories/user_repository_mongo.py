import asyncio
import logging

from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set
from core.infra.config.config_pydantic import get_settings
from core.infra.database.mongo_database import (
    MongoConnectionManager,
    MongoDocumentManager,
)
from core.infra.schemas.user_schema import UserDocument
from modules.user.domain.entities.user import CreateUserProps, RestoreUserProps, User
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


class UserRepositoryMongo(UserRepositoryProtocol):
    user_document: type[UserDocument]

    def __init__(self, user_document: type[UserDocument]) -> None:
        self.user_document = user_document

    async def create(self, entity: User) -> None:
        document = self.user_document(
            id=PydanticObjectId(entity.id),
            name=entity.props.name,
            email=entity.props.email,
            status=entity.props.status.value,
            password=entity.props.password.props.hashed_password,
            salt=entity.props.password.props.salt,
        )
        await document.insert()

    async def find_by_id(self, entity_id: str) -> User | None:
        user_document = await self.user_document.get(entity_id)
        if not user_document:
            return None
        return User.restore(
            id=str(user_document.id),
            props=RestoreUserProps(
                name=user_document.name,
                email=user_document.email,
                hashed_password=user_document.password,
                salt=user_document.salt,
                status=user_document.status,
            ),
        )

    async def find_all(self) -> list[User]:
        users_documents = await self.user_document.find().to_list()
        return [
            User.restore(
                id=str(user_document.id),
                props=RestoreUserProps(
                    name=user_document.name,
                    email=user_document.email,
                    hashed_password=user_document.password,
                    salt=user_document.salt,
                    status=user_document.status,
                ),
            )
            for user_document in users_documents
        ]

    async def update(self, entity: User) -> None:
        user = await self.user_document.find_one(
            self.user_document.id == PydanticObjectId(entity.id)
        )
        if not user:
            logging.warning("User not found")
            return None
        await user.update(
            Set(
                {
                    self.user_document.name: entity.props.name,
                    self.user_document.email: entity.props.email,
                }
            )
        )

    async def delete(self, entity_id: str) -> None:
        await self.user_document.find_one(
            self.user_document.id == PydanticObjectId(entity_id)
        ).delete()

    async def find_by_email(self, email: str) -> User | None:
        user_document = await self.user_document.find_one(
            self.user_document.email == email
        )
        if not user_document:
            return None
        return User.restore(
            id=str(user_document.id),
            props=RestoreUserProps(
                name=user_document.name,
                email=user_document.email,
                hashed_password=user_document.password,
                salt=user_document.salt,
                status=user_document.status,
            ),
        )

    async def bulk_create(self, entities: list[User]) -> None:
        documents = [
            self.user_document(
                name=entity.props.name,
                email=entity.props.email,
                status=entity.props.status.value,
                password=entity.props.password.props.hashed_password,
                salt=entity.props.password.props.salt,
            )
            for entity in entities
        ]
        await self.user_document.insert_many(documents)

    def next_id(self) -> str:
        return str(PydanticObjectId())


if __name__ == "__main__":

    async def main():
        settings = get_settings()
        document_manager = MongoDocumentManager()
        document_manager.add_document(UserDocument)
        connection_manager = MongoConnectionManager(settings.database_url)
        await connection_manager.connect("test", document_manager.documents)
        user_repository = UserRepositoryMongo(user_document=UserDocument)
        user_id = user_repository.next_id()
        user = User.create(
            user_id,
            props=CreateUserProps(
                name="User", email="mail@mail.com", password="password"
            ),
        )
        await user_repository.create(user)

    asyncio.run(main())
