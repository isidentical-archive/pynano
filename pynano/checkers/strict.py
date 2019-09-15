import ast
from typing import NoReturn

from pynano.checkers import NanoSyntaxError, SyntaxChecker
from pynano.interfaces import Precedence


class NotAllowedError(NanoSyntaxError):
    pass


class StrictSubsetChecker(SyntaxChecker):
    """Checks for if tree complies with pynano subset """

    ACTIVE = True
    PRECEDENCE = Precedence.INITAL

    def visit_Assign(self, node: ast.Assign) -> NoReturn:
        raise NotAllowedError(
            "Assignment statements without annotation is not allowed.", node
        )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # ignore pos and kw only
        arguments = node.args
        if any(arg.annotation is None for arg in arguments.args):
            raise NotAllowedError("Arguments without annotations is not allowed.", node)
        if node.returns is None:
            raise NotAllowedError(
                "Function definition without return type is not allowed.", node
            )
        return self.generic_visit(node)
