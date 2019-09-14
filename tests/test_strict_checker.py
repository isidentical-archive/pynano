import ast

import pytest

from pynano.checkers import NotAllowedError, StrictSubsetChecker


@pytest.fixture
def checker():
    StrictSubsetChecker.from_code = lambda s, c: s.check(ast.parse(c, "<test>", "exec"))
    checker = StrictSubsetChecker()
    return checker


def test_assignment(checker):
    assert checker.from_code("a: int = 5") is True
    with pytest.raises(NotAllowedError) as not_allowed_error:
        checker.from_code("a = 5")

    not_allowed_error = not_allowed_error.value
    assert not_allowed_error.msg.startswith("Assignment statements")


def test_valid_function_signature(checker):
    assert checker.from_code("def __test(a: int, b: int) -> str: pass") is True


@pytest.mark.parametrize(
    "signature", (["a", "b"], ["c: int", "d"], ["c: int", "d", "e: int"])
)
def test_invalid_function_signature_arguments(checker, signature):
    with pytest.raises(NotAllowedError) as not_allowed_error:
        checker.from_code("def __test({}) -> int: pass".format(", ".join(signature)))

    not_allowed_error = not_allowed_error.value
    assert not_allowed_error.msg.startswith("Arguments without")
