from pynano.checkers import NanoSyntaxError, SyntaxChecker


class NotAllowedError(NanoSyntaxError):
    pass


class StrictChecker(SyntaxChecker):
    """Checks for if tree complies with pynano subset """

    def visit_Assign(self, node):
        raise NotAllowedError(
            "Assignment statements without annotation is not allowed.", node
        )

    def visit_FunctionDef(self, node):
        # ignore pos and kw only
        arguments = node.args
        if not all(arg.annotation for arg in arguments.args):
            raise NotAllowedError("Arguments without annotations is not allowed.", node)
