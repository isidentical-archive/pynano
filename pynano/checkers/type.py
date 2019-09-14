from pynano.checkers import NanoSyntaxError, SyntaxChecker
from pynano.interfaces import Precedence


class NanoTypeError(NanoSyntaxError):
    pass


class TypeChecker(SyntaxChecker):
    """A very minimal type checker """

    ACTIVE = True
    PRECEDENCE = Precedence.FINAL
