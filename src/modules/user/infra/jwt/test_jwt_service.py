from typing import cast
from core.infra.config.config_pydantic import Settings
from modules.user.infra.jwt.jwt_service import JwtService


class FakeSettings:
    secret_key = "secret"


settings = cast(Settings, FakeSettings())


def test_jwt_service_create_token():
    jwt_service = JwtService(settings)
    token = jwt_service.create_token(id="any_id")
    assert token is not None


def test_jwt_service_verify_token():
    jwt_service = JwtService(settings)
    token = jwt_service.create_token(id="any_id")
    decoded = jwt_service.verify_token(token)
    assert decoded is not None
    assert decoded["sub"] == "any_id"
