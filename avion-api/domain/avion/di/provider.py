from typing import TypeVar, Generic, Type, Callable

T = TypeVar("T")


class Provider(Generic[T]):
    def __init__(self, typ: Type[T], callback: Callable[[Type[T], Type[T]], None]) -> None:
        self._type = typ
        self._callback = callback

    def using(self, cls: Type[T]) -> None:
        self._callback(self._type, cls)
