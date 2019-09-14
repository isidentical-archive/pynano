import ast

import pytest

from pynano.checkers import CHECKERS, NanoSyntaxError, SyntaxChecker


@pytest.fixture
def fake_checker():
    class FakeChecker(SyntaxChecker):
        ACTIVE = True

        def visit(self, node):
            for sub_node in ast.walk(node):
                if isinstance(sub_node, ast.Assign):
                    raise NanoSyntaxError("Not allowed", sub_node)
                continue

    return FakeChecker()


def test_nano_syntax_error():
    node = ast.parse("1", "<test>", "eval").body
    exc = NanoSyntaxError("test", node)
    assert exc.msg == "test"
    assert exc.filename is None
    assert exc.lineno == 1
    assert exc.offset == 0
    assert exc.text is None


def test_checker_subclass():
    class FakeChecker(SyntaxChecker):
        ACTIVE = True

    class FakeInactiveChecker(SyntaxChecker):
        pass

    assert FakeChecker in CHECKERS
    assert FakeInactiveChecker not in CHECKERS


def test_successful_check(fake_checker):
    tree = ast.parse("a: int = 5", "<test>", "exec")
    assert fake_checker.check(tree) is True


def test_unsuccessful_check(fake_checker):
    tree = ast.parse("a = 5", "<test>", "exec")
    exception = None
    with pytest.raises(NanoSyntaxError) as syntax_error:
        fake_checker.check(tree)

    syntax_error = syntax_error.value
    assert syntax_error.msg == "Not allowed"
    assert syntax_error.lineno == 1
    assert syntax_error.offset == 0
