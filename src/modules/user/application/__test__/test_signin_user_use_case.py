import logging
from modules.user.application.signin_user_use_case import (
    SigninUserInput,
    SigninUserOutput,
    SigninUserUseCase,
)
from modules.user.domain.entities.user import CreateUserProps, User
from modules.user.infra.jwt.jwt_service import JwtService
from modules.user.repositories.user_repository_in_memory import UserRepositoryInMemory
import pytest


class TestSigninUserUseCase:
    @pytest.mark.asyncio
    async def test_signin_user_use_case(self):
        user_repository = UserRepositoryInMemory()
        user_id = user_repository.next_id()
        user = User.create(
            user_id,
            CreateUserProps("any_name", "any_email", "any_password"),
        )
        await user_repository.create(user)
        jwt_service = JwtService("secret")
        use_case = SigninUserUseCase(
            user_repository=user_repository,
            jwt_service=jwt_service,
        )
        input = SigninUserInput(username="any_email", password="any_password")
        result = await use_case.handle(input)
        logging.warning(result)
        assert result.token is not None
        assert isinstance(result, SigninUserOutput)
