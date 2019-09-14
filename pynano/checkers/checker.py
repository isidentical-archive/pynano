import ast
from typing import Type, Union

ACTIVE_SIGN = "ACTIVE"
CHECKERS = []


class NanoSyntaxError(SyntaxError):
    # https://github.com/python/cpython/blob/5b9ff7a0dcb16d6f5c3cd4f1f52e0ca6a4bde586/Objects/exceptions.c#L1355

    def __init__(self, msg: str, node: ast.AST) -> None:
        super().__init__(msg, (None, node.lineno, node.col_offset, None))


class SyntaxChecker(ast.NodeVisitor):
    def __init_subclass__(cls: Type[SyntaxChecker]) -> None:
        if getattr(cls, ACTIVE_SIGN, None):
            CHECKERS.append(cls)

    def check(self, tree: ast.AST, *, strict: bool = True) -> bool:
        return self.visit(tree) or True
