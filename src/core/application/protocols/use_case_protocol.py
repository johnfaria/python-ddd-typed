from abc import abstractmethod
from typing import Protocol


class UseCaseProtocol[Input, Output](Protocol):
    @abstractmethod
    async def handle(self, input: Input) -> Output: ...
