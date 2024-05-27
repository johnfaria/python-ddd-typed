import logging
import pytest
import pytest_asyncio
from core.infra.database.mongo_database import (
    MongoConnectionManager,
    MongoDocumentManager,
)
from core.infra.schemas.user_schema import UserDocument
from modules.user.domain.user import User, UserProps
from modules.user.repositories.user_repository_mongo import UserRepositoryMongo
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@pytest_asyncio.fixture
async def user_repository(mongodb_container):
    url = mongodb_container.get_connection_url()
    document = UserDocument
    document_manager = MongoDocumentManager()
    document_manager.add_document(document=document)
    connection_manager = MongoConnectionManager(url)
    await connection_manager.connect("test", document_manager.documents)
    user_repository = UserRepositoryMongo(user_document=document)
    yield user_repository
    await document.delete_all()
    await connection_manager.disconnect()


class TestUserRepositoryMongo:
    @pytest.mark.asyncio
    async def test_user_repository_in_memory_create(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = user_repository.next_id()
        user = User.create(user_id, user_props)
        await user_repository.create(user)
        user_from_repo = await user_repository.find_by_id(user.id)
        if user_from_repo is None:
            assert False
        assert user.equals(user_from_repo)

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_by_id(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = user_repository.next_id()
        user = User.create(user_id, user_props)
        await user_repository.create(user)
        user_from_repo = await user_repository.find_by_id(user.id)
        if user_from_repo is None:
            assert False
        assert user.equals(user_from_repo)

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_by_email(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = user_repository.next_id()
        user = User.create(user_id, user_props)
        await user_repository.create(user)
        user_from_repo = await user_repository.find_by_email(user.props.email)
        if user_from_repo is None:
            assert False
        assert user.equals(user_from_repo)

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_all(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = user_repository.next_id()
        user = User.create(user_id, user_props)
        await user_repository.create(user)
        users_from_repo = await user_repository.find_all()
        assert len(users_from_repo) == 1
        assert user.equals(users_from_repo[0])

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_delete(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = user_repository.next_id()
        user = User.create(user_id, user_props)
        await user_repository.create(user)
        await user_repository.delete(user.id)
        entities = await user_repository.find_all()
        assert entities == []

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_update(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = user_repository.next_id()
        user = User.create(user_id, user_props)
        await user_repository.create(user)
        user_from_repository = await user_repository.find_by_id(user.id)
        if user_from_repository is None:
            assert False
        user_from_repository.deactivate()
        await user_repository.update(user_from_repository)
        entities = await user_repository.find_all()
        assert user_from_repository.equals(entities[0])

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_bulk_create(
        self, user_repository: UserRepositoryProtocol
    ):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_repository.next_id(), user_props)
        users = [User.create(user_repository.next_id(), user_props) for _ in range(10)]
        await user_repository.bulk_create([user])
        entities = await user_repository.find_all()
        assert len(entities) == 1
        await user_repository.bulk_create(users)
        entities = await user_repository.find_all()
        assert len(entities) == 11
