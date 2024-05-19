from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class UseCaseProtocol[Input, Output](Protocol):
    @abstractmethod
    async def handle(self, input: Input) -> Output: ...
