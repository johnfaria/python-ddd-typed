from core.infra.config.config_pydantic import get_settings
from core.infra.schemas.user_schema import UserDocument
from fastapi import Depends
from typing import AsyncGenerator
from modules.user.application.create_customer_use_case import CreateUserUseCase
from modules.user.application.list_users_use_case import ListUsersUseCase
from modules.user.application.signin_user_use_case import SigninUserUseCase
from modules.user.application.update_user_use_case import UpdateUserUseCase
from modules.user.domain.services.jwt_service_protocol import JwtServiceProtocol
from modules.user.infra.jwt.jwt_service import JwtService
from modules.user.repositories.user_repository_mongo import UserRepositoryMongo
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


class UserServiceProviders:
    @staticmethod
    async def get_jwt_service() -> AsyncGenerator[JwtServiceProtocol, None]:
        yield JwtService(settings=get_settings())


class UserRepositoryProviders:
    @staticmethod
    async def get_user_repository() -> AsyncGenerator[UserRepositoryProtocol, None]:
        user_repository = UserRepositoryMongo(user_document=UserDocument)
        yield user_repository


class UserUseCaseProviders:
    @staticmethod
    async def get_list_users_use_case(
        user_repository: UserRepositoryProtocol = Depends(
            UserRepositoryProviders.get_user_repository
        ),
    ) -> AsyncGenerator[ListUsersUseCase, None]:
        yield ListUsersUseCase(user_repository)

    @staticmethod
    async def get_create_user_use_case(
        user_repository: UserRepositoryProtocol = Depends(
            UserRepositoryProviders.get_user_repository
        ),
    ) -> AsyncGenerator[CreateUserUseCase, None]:
        yield CreateUserUseCase(user_repository)

    @staticmethod
    async def get_signin_user_use_case(
        user_repository: UserRepositoryProtocol = Depends(
            UserRepositoryProviders.get_user_repository
        ),
        jwt_service: JwtServiceProtocol = Depends(UserServiceProviders.get_jwt_service),
    ) -> AsyncGenerator[SigninUserUseCase, None]:
        yield SigninUserUseCase(user_repository, jwt_service)

    @staticmethod
    async def get_update_user_use_case(
        user_repository: UserRepositoryProtocol = Depends(
            UserRepositoryProviders.get_user_repository
        ),
    ) -> AsyncGenerator[UpdateUserUseCase, None]:
        yield UpdateUserUseCase(user_repository)


class UserModuleProviders:
    use_cases = UserUseCaseProviders
    repositories = UserRepositoryProviders
