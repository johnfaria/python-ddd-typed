from src.modules.user.domain.user import User, UserProps
from src.modules.user.repositories.user_repository_in_memory import (
    UserRepositoryInMemory,
)


class TestUserRepositoryInMemory:
    user_repository: UserRepositoryInMemory

    def setup_method(self):
        self.user_repository = UserRepositoryInMemory()

    def test_user_repository_in_memory_create(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        self.user_repository.create(user)
        assert self.user_repository.entities[0] == user

    def test_user_repository_in_memory_find_by_id(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        self.user_repository.create(user)
        assert self.user_repository.find_by_id(user.id) == user

    def test_user_repository_in_memory_find_by_email(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        self.user_repository.create(user)
        assert self.user_repository.find_by_email(user.props.email) == user

    def test_user_repository_in_memory_find_all(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        self.user_repository.create(user)
        assert self.user_repository.find_all() == [user]

    def test_user_repository_in_memory_delete(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        self.user_repository.create(user)
        self.user_repository.delete(user.id)
        assert self.user_repository.entities == []

    def test_user_repository_in_memory_update(self):
        user_props = UserProps(
            name="any_name", email="any_email", password="any_password"
        )
        user = User.create(user_props)
        self.user_repository.create(user)
        user_from_repository = self.user_repository.find_by_id(user.id)
        if user_from_repository is None:
            assert False
        user_from_repository.deactivate()
        self.user_repository.update(user_from_repository)
        assert self.user_repository.entities[0] == user_from_repository
