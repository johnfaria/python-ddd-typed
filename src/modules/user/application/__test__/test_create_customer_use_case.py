from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.application.create_customer_use_case import (
    CreateUserInput,
    CreateUserUseCase,
)
from modules.user.repositories.user_repository_in_memory import UserRepositoryInMemory
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol
import pytest


class TestCreateCustomerUseCase:
    user_repository: UserRepositoryProtocol

    def setup_method(self):
        self.user_repository = UserRepositoryInMemory()

    def test_create_customer_use_case_instance(self):
        create_customer_use_case = CreateUserUseCase(self.user_repository)
        assert isinstance(create_customer_use_case, CreateUserUseCase)
        assert isinstance(create_customer_use_case, UseCaseProtocol)

    @pytest.mark.asyncio
    async def test_create_customer(self):
        create_customer_use_case = CreateUserUseCase(self.user_repository)
        input = CreateUserInput(
            name="any_name", email="any_email", password="any_password"
        )
        output = await create_customer_use_case.handle(input)
        assert output.id is not None
        assert output.name == "any_name"
        assert output.email == "any_email"
        assert output.status == "active"

    @pytest.mark.asyncio
    async def test_should_not_create_customer_with_duplicated_email(self):
        create_customer_use_case = CreateUserUseCase(self.user_repository)
        input = CreateUserInput(
            name="any_name", email="any_email", password="any_password"
        )
        await create_customer_use_case.handle(input)
        try:
            await create_customer_use_case.handle(input)
        except ValueError as error:
            assert str(error) == "User already exists"
        else:
            assert False
