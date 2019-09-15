import ast
from collections import UserDict
from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto
from typing import Any, Mapping, Optional

Namespace = Mapping[str, str]


class Precedence(IntEnum):
    INITAL = 0
    LOW = 1
    AVG = 2
    HAVG = 3
    FINAL = 4


class Scopes(Enum):
    LOCAL = auto()
    MODULE = auto()


class NanoError(SyntaxError):
    # https://github.com/python/cpython/blob/5b9ff7a0dcb16d6f5c3cd4f1f52e0ca6a4bde586/Objects/exceptions.c#L1355

    def __init__(self, msg: str, node: ast.AST) -> None:
        super().__init__(msg, (None, node.lineno, node.col_offset, None))


class NanoSymbolError(NanoError):
    pass


class NamespaceDict(UserDict):
    def __setitem__(self, item: Any, value: Any) -> None:
        return super().__setitem__(str(item), value)

    def __getitem__(self, item: Any) -> Any:
        return super().__getitem__(str(item))


@dataclass
class Scope:
    local: Namespace = field(default_factory=NamespaceDict)
    module: Namespace = field(default_factory=NamespaceDict)


def parse(node: Optional[ast.expr]) -> str:  # type: ignore
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant) and node.value is None:
        return None
