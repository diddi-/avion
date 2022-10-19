from inspect import signature
from typing import TypeVar, Dict, Type, cast, Any

from avion.di.provider import Provider

T = TypeVar("T")

class Container:
    def __init__(self) -> None:
        self._providers: Dict[Any, Any] = {}

    def _provider_callback(self, typ: Type[T], cls: Type[T]) -> None:
        self._providers[typ] = cls

    def resolve(self, typ: Type[T]) -> Provider[T]:
        return Provider[T](typ, self._provider_callback)

    def get_instance(self, typ: Type[T]) -> T:
        cls = self._providers[typ]
        sig = signature(cls.__init__)
        args = []
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param.annotation in self._providers.keys():
                if param.kind == param.POSITIONAL_OR_KEYWORD or param.kind == param.POSITIONAL_ONLY:
                    args.append(self.get_instance(param.annotation))
                else:
                    kwargs[param_name] = self.get_instance(param.annotation)
        return cast(T, cls(*args, **kwargs))
