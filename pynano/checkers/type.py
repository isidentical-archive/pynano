import ast

from pynano.checkers import NanoSyntaxError, SyntaxChecker
from pynano.interfaces import Precedence, parse


class NanoTypeError(NanoSyntaxError):
    pass


VALID_TYPES = {"integer", "float"}


class TypeValidator(SyntaxChecker):
    """ Validates types according to PyNano spec """

    ACTIVE = True
    PRECEDENCE = Precedence.FINAL

    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        if parse(node.annotation) not in VALID_TYPES:
            raise NanoTypeError("Invalid type for assignment target.", node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if any(parse(arg.annotation) not in VALID_TYPES for arg in node.args.args):
            raise NanoTypeError("Invalid type for argument.", node)
        if parse(node.returns) not in VALID_TYPES:
            raise NanoTypeError("Invalid type for return signature.", node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if all(
            isinstance(getattr(node, side), ast.Constant) for side in {"left", "right"}
        ):
            if type(node.left.value) is not type(node.right.value):
                raise NanoTypeError(
                    "Both left and right hand side of arithmetical operations should have same type.",
                    node,
                )
