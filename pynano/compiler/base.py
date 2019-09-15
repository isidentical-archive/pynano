import ast

from pynano.interfaces import NanoError


class Compiler(ast.NodeTransformer):
    def compile(self, tree: ast.AST) -> str:
        code = self.visit(tree)
        return code


class CompilationError(NanoError):
    pass
