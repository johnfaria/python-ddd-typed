from dataclasses import dataclass

from core.application.protocols.use_case_protocol import UseCaseProtocol
from modules.user.domain.services.jwt_service_protocol import JwtServiceProtocol
from modules.user.repositories.user_repository_protocol import UserRepositoryProtocol


@dataclass
class SigninUserInput:
    email: str
    password: str


@dataclass
class SigninUserOutput:
    token: str


class SigninUserUseCase(UseCaseProtocol[SigninUserInput, SigninUserOutput]):
    def __init__(
        self, user_repository: UserRepositoryProtocol, jwt_service: JwtServiceProtocol
    ):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def handle(self, input: SigninUserInput) -> SigninUserOutput:
        user = await self.user_repository.find_by_email(input.email)
        if not user:
            raise ValueError("User not found")
        if not user.verify_password(input.password):
            raise ValueError("Invalid password")
        token = self.jwt_service.create_token(user.id)
        return SigninUserOutput(token)
