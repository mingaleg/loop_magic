from contextlib import AbstractContextManager
from dataclasses import dataclass
from types import TracebackType
from typing import Optional
from typing_extensions import Never


@dataclass(frozen=True)
class CodeBlockInterruption(BaseException):
    singleton: object


class CodeBlock(AbstractContextManager):
    def __init__(self):
        self._singleton = object()
        self._exited = False

    def exit(self) -> Never:
        if self._exited:
            raise AssertionError("Trying to exit from an already exited CodeBlock")
        raise CodeBlockInterruption(self._singleton)

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if not isinstance(exc_value, CodeBlockInterruption):
            return False
        self._exited = True
        return exc_value.singleton is self._singleton
