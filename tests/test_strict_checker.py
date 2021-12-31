import ast

import pytest

from pynano.checkers import NotAllowedError, StrictSubsetChecker


@pytest.fixture
def checker():
    return StrictSubsetChecker()


def test_assignment(checker):
    assert checker.code_check("a: int = 5") is True
    with pytest.raises(NotAllowedError) as not_allowed_error:
        checker.code_check("a = 5")

    not_allowed_error = not_allowed_error.value
    assert not_allowed_error.msg.startswith("Assignment statements")


def test_valid_function_signature(checker):
    assert (
        checker.code_check("def __test(a: int, b: int) -> str: pass") is True
    )


@pytest.mark.parametrize(
    "signature", (["a", "b"], ["c: int", "d"], ["c: int", "d", "e: int"])
)
def test_invalid_function_signature_arguments(checker, signature):
    with pytest.raises(NotAllowedError) as not_allowed_error:
        checker.code_check(
            "def __test({}) -> int: pass".format(", ".join(signature))
        )

    not_allowed_error = not_allowed_error.value
    assert not_allowed_error.msg.startswith("Arguments without")


def test_invalid_function_signature_return(checker):
    with pytest.raises(NotAllowedError) as not_allowed_error:
        checker.code_check("def __test(a: int): pass")

    not_allowed_error = not_allowed_error.value
    assert not_allowed_error.msg.startswith(
        "Function definition without return type"
    )
