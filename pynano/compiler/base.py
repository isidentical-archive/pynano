import ast
from functools import wraps
from typing import Callable

from pynano.interfaces import NanoError, Scope, Scopes


class Compiler(ast.NodeTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scope = Scopes.MODULE
        self._symbol_table = Scope()

    def compile(self, tree: ast.AST) -> str:
        code = self.visit(tree)
        return code


class CompilationError(NanoError):
    pass


def context_change(func: Callable[[Compiler, ast.AST], "Instruction"]):
    @wraps(func)
    def wrapper(self: Compiler, node: ast.AST) -> "Instruction":
        self._symbol_table.local.clear()
        self._scope = Scopes.LOCAL
        result = func(self, node)
        self._scope = Scopes.MODULE
        self._symbol_table.local.clear()
        return result

    return wrapper
