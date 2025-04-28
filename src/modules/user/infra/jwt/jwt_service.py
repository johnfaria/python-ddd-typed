from datetime import datetime, timedelta, timezone
from typing import Any

from core.infra.config.config_pydantic import Settings, get_settings
import jwt
from modules.user.domain.services.jwt_service_protocol import (
    JwtServiceProtocol,
    require_auth,
)
from functools import partial


class JwtService(JwtServiceProtocol):
    def __init__(self, settings: Settings):
        self.settings = settings

    def create_token(self, id: str) -> str:
        payload = {
            "sub": id,
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(days=1),
        }
        return jwt.encode(
            payload,
            self.settings.secret_key,
            algorithm="HS256",
        )

    def verify_token(self, token: str) -> dict[str, Any] | None:
        try:
            return jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=["HS256"],
            )
        except Exception:
            return None


require_auth_jwt = partial(
    require_auth,
    jwt_service=JwtService(get_settings()),
)
