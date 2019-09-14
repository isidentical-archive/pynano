import ast


class Compiler(ast.NodeTransformer):
    def compile(self, tree: ast.AST) -> str:
        code = self.visit(tree)
        return code


class CompilationError(Exception):
    pass
