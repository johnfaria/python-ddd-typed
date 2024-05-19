import pytest

from src.modules.user.domain.user import User, UserProps
from src.modules.user.repositories.user_repository_in_memory import (
    UserRepositoryInMemory,
)

@pytest.mark.asyncio
async def test_user_repository_in_memory_create():
    user_repository = UserRepositoryInMemory()
    user_props = UserProps(
        name="any_name", email="any_email", password="any_password"
    )
    user = User.create(user_props)
    await user_repository.create(user)
    assert user_repository.entities[0] == user

class TestUserRepositoryInMemory:
    user_repository: UserRepositoryInMemory

    def setup_method(self):
        self.user_repository = UserRepositoryInMemory()

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_create(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        await self.user_repository.create(user)
        assert self.user_repository.entities[0] == user

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_by_id(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        await self.user_repository.create(user)
        assert await self.user_repository.find_by_id(user.id) == user

    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_by_email(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        await self.user_repository.create(user)
        assert await self.user_repository.find_by_email(user.props.email) == user
        
    @pytest.mark.asyncio
    async def test_user_repository_in_memory_find_all(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        await self.user_repository.create(user)
        assert await self.user_repository.find_all() == [user]
        
    @pytest.mark.asyncio
    async def test_user_repository_in_memory_delete(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        await self.user_repository.create(user)
        await self.user_repository.delete(user.id)
        assert self.user_repository.entities == []
        
    @pytest.mark.asyncio
    async def test_user_repository_in_memory_update(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        await self.user_repository.create(user)
        user_from_repository = await self.user_repository.find_by_id(user.id)
        if user_from_repository is None:
            assert False
        user_from_repository.deactivate()
        await self.user_repository.update(user_from_repository)
        assert self.user_repository.entities[0] == user_from_repository
