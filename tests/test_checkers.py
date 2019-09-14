import ast

from pynano.checkers import CHECKERS, NanoSyntaxError, SyntaxChecker


def test_nano_syntax_error():
    node = ast.parse("1", "<test>", "eval").body
    exc = NanoSyntaxError("test", node)
    assert exc.msg == "test"
    assert exc.filename is None
    assert exc.lineno == 1
    assert exc.offset == 0
    assert exc.text is None
