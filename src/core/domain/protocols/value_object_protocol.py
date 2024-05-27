from typing import Protocol


class ValueObject[T](Protocol):
    props: T

    def __init__(self, props: T) -> None:
        self.props = props

    def equals(self, vo: "ValueObject[T]") -> bool:
        return self.props == vo.props
