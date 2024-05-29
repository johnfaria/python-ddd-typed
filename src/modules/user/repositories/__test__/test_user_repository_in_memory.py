import pytest

from modules.user.domain.entities.user import CreateUserProps, User
from modules.user.repositories.user_repository_in_memory import (
    UserRepositoryInMemory,
)


class TestUserRepositoryInMemory:
    user_repository: UserRepositoryInMemory

    def setup_method(self):
        self.user_repository = UserRepositoryInMemory()

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_create(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = self.user_repository.next_id()
        user = User.create(user_id, user_props)
        await self.user_repository.create(user)
        assert self.user_repository.entities[0] == user

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_by_id(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = self.user_repository.next_id()
        user = User.create(user_id, user_props)
        await self.user_repository.create(user)
        assert await self.user_repository.find_by_id(user.id) == user

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_by_email(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = self.user_repository.next_id()
        user = User.create(user_id, user_props)
        await self.user_repository.create(user)
        assert await self.user_repository.find_by_email(user.props.email) == user

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_all(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = self.user_repository.next_id()
        user = User.create(user_id, user_props)
        await self.user_repository.create(user)
        assert await self.user_repository.find_all() == [user]

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_delete(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = self.user_repository.next_id()
        user = User.create(user_id, user_props)
        await self.user_repository.create(user)
        await self.user_repository.delete(user.id)
        assert self.user_repository.entities == []

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_update(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user_id = self.user_repository.next_id()
        user = User.create(user_id, user_props)
        await self.user_repository.create(user)
        user_from_repository = await self.user_repository.find_by_id(user.id)
        if user_from_repository is None:
            assert False
        user_from_repository.deactivate()
        await self.user_repository.update(user_from_repository)
        assert self.user_repository.entities[0] == user_from_repository

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_bulk_create(self):
        user_props = CreateUserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(self.user_repository.next_id(), user_props)
        users = [
            User.create(self.user_repository.next_id(), user_props) for _ in range(10)
        ]
        await self.user_repository.bulk_create([user])
        assert self.user_repository.entities[0] == user
        assert len(self.user_repository.entities) == 1
        await self.user_repository.bulk_create(users)
        assert self.user_repository.entities == [user] + users
        assert len(self.user_repository.entities) == 11
