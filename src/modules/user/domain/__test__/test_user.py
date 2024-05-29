from modules.user.domain.value_objects.password_vo import Password
from modules.user.domain.entities.user import CreateUserProps, RestoreUserProps, User


class TestUserAggregate:
    def test_create_user_aggregate(self):
        user_props = CreateUserProps(
            name="John Doe",
            email="mail@email.com",
            password="secret",
        )
        user = User.create("id", user_props)
        assert isinstance(user, User)

    def test_restore_user_aggregate(self):
        user_props = RestoreUserProps(
            name="John Doe",
            email="mail@email.com",
            hashed_password="",
            salt="",
            status="inactive",
        )
        user = User.restore("id", user_props)
        assert isinstance(user, User)

    def test_user_aggregate_password_validation_from_restore(self):
        password = Password.create("secret")
        user_props = RestoreUserProps(
            name="John Doe",
            email="mail@email.com",
            hashed_password=password.props.hashed_password,
            salt=password.props.salt,
            status="inactive",
        )
        user = User.restore("id", user_props)
        assert user.verify_password("secret")

    def test_user_aggregate_password_validation_from_create(self):
        user_props = CreateUserProps(
            name="John Doe",
            email="mail@email.com",
            password="secret",
        )
        user = User.create("id", user_props)
        assert user.verify_password("secret")
