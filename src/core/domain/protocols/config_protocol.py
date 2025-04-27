from typing import Protocol, runtime_checkable


@runtime_checkable
class ConfigProtocol(Protocol):
    database_url: str
    database_name: str
    secret_key: str
    environment: str
