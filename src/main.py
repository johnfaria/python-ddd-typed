import asyncio

from modules.user.application.create_customer_use_case import (
    CreateCustomerInput,
    CreateCustomerUseCase,
)
from modules.user.repositories.user_repository_in_memory import UserRepositoryInMemory


async def main():
    repository = UserRepositoryInMemory()
    use_case = CreateCustomerUseCase(repository)
    input = CreateCustomerInput(name="John Doe", email="email", password="password")
    result = await use_case.handle(input)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
