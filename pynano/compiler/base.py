import ast


class Compiler(ast.NodeTransformer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = []

    def compile(self, tree):
        code = self.visit(tree)
        return code


class CompilationError(Exception):
    pass
