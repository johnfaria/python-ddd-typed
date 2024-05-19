from abc import abstractmethod
from collections.abc import Awaitable
from typing import Protocol, runtime_checkable


@runtime_checkable
class UseCaseProtocol[Input, Output](Protocol):
    @abstractmethod
    def handle(self, input: Input) -> Awaitable[Output] | Output: ...
