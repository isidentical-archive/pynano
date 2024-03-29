from __future__ import annotations

import ast
from typing import Type, Union

from pynano.interfaces import NanoError, Precedence

ACTIVE_SIGN = "ACTIVE"
PRECEDENCE_SIGN = "PRECEDENCE"
CHECKERS = []


class NanoSyntaxError(NanoError):
    pass


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
