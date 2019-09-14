from pynano.checkers import NanoSyntaxError, SyntaxChecker


class NanoTypeError(NanoSyntaxError):
    pass


class TypeChecker(SyntaxChecker):
    """A very minimal type checker """

    ACTIVE = True
