from __future__ import annotations

import ast
from typing import Type, Union

from pynano.interfaces import Precedence

ACTIVE_SIGN = "ACTIVE"
PRECEDENCE_SIGN = "PRECEDENCE"
CHECKERS = []


class NanoSyntaxError(SyntaxError):
    # https://github.com/python/cpython/blob/5b9ff7a0dcb16d6f5c3cd4f1f52e0ca6a4bde586/Objects/exceptions.c#L1355

    def __init__(self, msg: str, node: ast.AST) -> None:
        super().__init__(msg, (None, node.lineno, node.col_offset, None))


class SyntaxChecker(ast.NodeVisitor):
    ACTIVE = False
    PRECEDENCE = Precedence.AVG

    def __init_subclass__(cls: Type[SyntaxChecker]) -> None:
        if getattr(cls, ACTIVE_SIGN):
            CHECKERS.append(cls)
            CHECKERS.sort(key=lambda cls: getattr(cls, PRECEDENCE_SIGN))

    def check(self, tree: ast.AST, *, strict: bool = True) -> bool:
        return self.visit(tree) or True

    def code_check(self, code: str) -> bool:
        return self.check(ast.parse(code, "<test>", "exec"))
