from typing import Protocol


class UseCaseProtocol[Input, Output](Protocol):
    async def handle(self, input: Input) -> Output: ...
