from inspect import signature
from typing import TypeVar, Dict, Type

from avion.di.provider import Provider

T = TypeVar("T")


class Container:
    def __init__(self) -> None:
        self._providers: Dict[Type[T], Type[T]] = {}

    def _provider_callback(self, typ: Type[T], cls: Type[T]) -> None:
        self._providers[typ] = cls

    def resolve(self, typ: Type[T]) -> Provider[T]:
        return Provider[T](typ, self._provider_callback)

    def get_instance(self, typ: Type[T]) -> T:
        cls = self._providers[typ]
        sig = signature(cls.__init__)
        args = []
        kwargs = {}
        for p, t in sig.parameters.items():
            if t.annotation in self._providers.keys():
                if t.kind == t.POSITIONAL_OR_KEYWORD or t.kind == t.POSITIONAL_ONLY:
                    args.append(self.get_instance(t.annotation))
                else:
                    kwargs[p] = self.get_instance(t.annotation)
        return cls(*args, **kwargs)
