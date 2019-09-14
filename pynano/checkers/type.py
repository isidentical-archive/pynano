from pynano.checkers import NanoSyntaxError, SyntaxChecker
from pynano.interfaces import Precedence


class NanoTypeError(NanoSyntaxError):
    pass


VALID_TYPES = {"integer", "float"}


class TypeValidator(SyntaxChecker):
    """ Validates types according to PyNano spec """

    ACTIVE = True
    PRECEDENCE = Precedence.FINAL

    def visit_AnnAssign(self, node):
        if node.annotation.id not in VALID_TYPES:
            raise NanoTypeError("Invalid type for assignment target.", node)

    def visit_FunctionDef(self, node):
        if any(arg.annotation.id not in VALID_TYPES for arg in node.args.args):
            raise NanoTypeError("Invalid type for argument.", node)
        if node.returns.id not in VALID_TYPES:
            raise NanoTypeError("Invalid type for return signature.", node)
