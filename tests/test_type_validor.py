import pytest

from pynano.checkers import VALID_TYPES, NanoTypeError, TypeValidator


@pytest.fixture
def checker():
    return TypeValidator()


@pytest.mark.parametrize("valid_type", VALID_TYPES)
def test_valid_type(checker, valid_type):
    assert checker.code_check(f"a: {valid_type} = bla_bla") is True
    assert (
        checker.code_check(f"def __test(a: {valid_type}) -> {valid_type}: pass") is True
    )


def test_invalid_assignment(checker):
    with pytest.raises(NanoTypeError) as type_error:
        checker.code_check("a: __bla_bla = bla_bla")

    type_error = type_error.value
    assert type_error.msg.endswith("assignment target.")


@pytest.mark.parametrize("signature", (["integer", "bla_bla"], ["bla_bla", "float"]))
def test_invalid_function_signature_arguments(checker, signature):
    with pytest.raises(NanoTypeError) as type_error:
        checker.code_check(
            "def __test(a: {}, b: {}) -> integer: pass".format(*signature)
        )

    type_error = type_error.value
    assert type_error.msg.endswith("argument.")


def test_invalid_function_signature_return(checker):
    with pytest.raises(NanoTypeError) as type_error:
        checker.code_check("def __test(a: integer, b: float) -> string: pass")

    type_error = type_error.value
    assert type_error.msg.endswith("return signature.")
