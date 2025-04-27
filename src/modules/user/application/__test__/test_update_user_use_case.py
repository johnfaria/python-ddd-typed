import logging

import pytest
from core.infra.config.config_pydantic import get_settings
from modules.user.application.signin_user_use_case import (
    SigninUserInput,
    SigninUserUseCase,
)
from modules.user.application.update_user_use_case import (
    UpdateUserInput,
    UpdateUserUseCase,
)
from modules.user.domain.entities.user import CreateUserProps, User
from modules.user.infra.jwt.jwt_service import JwtService
from modules.user.repositories.user_repository_in_memory import UserRepositoryInMemory


class TestUpdateUserUseCase:
    @pytest.mark.asyncio
    async def test_update_user(self):
        jwt_service = JwtService(get_settings())
        user_repository = UserRepositoryInMemory()
        user_id = user_repository.next_id()
        user = User.create(
            user_id,
            CreateUserProps("any_name", "any_email", "any_password"),
        )
        user_id2 = user_repository.next_id()
        user2 = User.create(
            user_id2,
            CreateUserProps("any_name", "any_email", "any_password"),
        )
        await user_repository.create(user)
        await user_repository.create(user2)

        signin_user_input = SigninUserInput(
            email="any_email",
            password="any_password",
        )

        signin_user_use_case = SigninUserUseCase(
            user_repository=user_repository,
            jwt_service=jwt_service,
        )

        signin_user_result = await signin_user_use_case.handle(signin_user_input)

        logging.warning(signin_user_result)

        use_case = UpdateUserUseCase(user_repository)
        input = UpdateUserInput(
            token=signin_user_result.token,
            id=user.id,
            name="any_name_updated",
            email="any_email_updated",
            password="any_password_updated",
        )
        await use_case.handle(input)

        user = await user_repository.find_by_id(user.id)
        if user:
            logging.warning(user.props)

        assert user is not None
        assert user.props.name == "any_name_updated"
        assert user.props.email == "any_email_updated"
