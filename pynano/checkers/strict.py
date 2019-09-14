from pynano.checkers import NanoSyntaxError, SyntaxChecker


class NotAllowedError(NanoSyntaxError):
    pass


class StrictSubsetChecker(SyntaxChecker):
    """Checks for if tree complies with pynano subset """

    ACTIVE = True

    def visit_Assign(self, node):
        raise NotAllowedError(
            "Assignment statements without annotation is not allowed.", node
        )

    def visit_FunctionDef(self, node):
        # ignore pos and kw only
        arguments = node.args
        if not all(arg.annotation for arg in arguments.args):
            raise NotAllowedError("Arguments without annotations is not allowed.", node)
        if node.returns is None:
            raise NotAllowedError(
                "Function definition without return type is not allowed.", node
            )
        return self.generic_visit(node)
