from typing import Protocol, runtime_checkable


@runtime_checkable
class ConfigProtocol(Protocol):
    database_url: str
    secret_key: str
    envinroment: str
