import ast
from typing import Union

ACTIVE_SIGN = "active"
CHECKERS = []


class NanoSyntaxError(SyntaxError):
    # https://github.com/python/cpython/blob/5b9ff7a0dcb16d6f5c3cd4f1f52e0ca6a4bde586/Objects/exceptions.c#L1355

    def __init__(self, msg, filename, lineno, offset, text):
        super().__init__(msg, (filename, lineno, offset, text))


class SyntaxChecker(ast.NodeVisitor):
    def __init_subclass__(cls):
        if getattr(cls, ACTIVE_SIGN, None):
            CHECKERS.append(cls)

    def check(self, tree, strict=False) -> Union[bool, NanoSyntaxError]:
        try:
            self.visit(tree)
        except NanoSyntaxError as exc:
            return exc
        else:
            return True
