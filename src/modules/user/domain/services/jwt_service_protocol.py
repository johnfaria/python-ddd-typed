from abc import abstractmethod
from functools import wraps
from typing import Any, Callable, NamedTuple, Protocol, runtime_checkable


class JwtPayload(NamedTuple):
    sub: str
    iat: int
    exp: int

@runtime_checkable
class JwtServiceProtocol(Protocol):
    @abstractmethod
    def create_token(self, id: str) -> str: ...

    @abstractmethod
    def verify_token(self, token: str) -> dict | None: ...


def require_auth(
    func: Callable[..., Any],
    jwt_service: JwtServiceProtocol,
) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        input = args[1]
        payload = jwt_service.verify_token(input.token)
        if payload is None or payload["sub"] != input.id:
            raise ValueError("Unauthorized")
        value = func(*args, **kwargs)
        return value

    return wrapper
