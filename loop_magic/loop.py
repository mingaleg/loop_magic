import ast
from collections.abc import Iterable
from contextlib import AbstractContextManager
from dataclasses import dataclass
import inspect
import textwrap
from types import TracebackType
import types
from typing import Callable, Generic, Optional, TypeVar
from typing_extensions import Literal, Never, ParamSpec

from more_itertools import one

from .loop_ast_transformer import LoopAstTransformer
from .code_block import CodeBlock
from .exceptions import CriticalLoopException


_T = TypeVar("_T")
_P = ParamSpec("_P")
_R = TypeVar("_R")


@dataclass(frozen=True)
class LoopControl:
    outer_block: CodeBlock
    inner_block: CodeBlock

    def break_(self) -> Never:
        self.outer_block.exit()

    def continue_(self) -> Never:
        self.inner_block.exit()


class Loop(AbstractContextManager, Generic[_T]):
    code_block: type[CodeBlock] = CodeBlock
    loop_control: type[LoopControl] = LoopControl

    def __init__(self, iter: Iterable[_T]):
        self.iter = iter

    def __enter__(self) -> tuple[_T, LoopControl]:
        raise CriticalLoopException("To use Loop annotate the function using it with @Loop.enable")

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Literal[False]:
        return False

    @staticmethod
    def enable(func: Callable[_P, _R]) -> Callable[_P, _R]:
        func_ast = ast.parse(textwrap.dedent(inspect.getsource(func)))

        patched_ast = LoopAstTransformer().visit(func_ast)
        ast.fix_missing_locations(patched_ast)

        new_code = compile(patched_ast, func.__code__.co_filename, "exec")
        new_func_code = one(co for co in new_code.co_consts if isinstance(co, types.CodeType))

        new_func = types.FunctionType(new_func_code, globals(), func.__name__, func.__defaults__, func.__closure__)
        return new_func
