from pathlib import Path

import pytest

from pynano.checkers import SyntaxChecker
from pynano.pyn import PyNano

BASE_PATH = Path(__file__).parent.resolve()


@pytest.fixture
def pynano():
    return PyNano()


def test_pynano_differnet_checkers():
    class FakeChecker(SyntaxChecker):
        ACTIVE = False

    pyn = PyNano([FakeChecker])
    assert isinstance(pyn.checkers[0], FakeChecker)


@pytest.mark.parametrize(
    "program",
    (
        BASE_PATH / "examples" / "empty.pyn",
        BASE_PATH / "examples" / "demo_func.pyn",
    ),
)
def test_pynano_example(pynano, program):
    result = pynano.compile(program)
    assert result is not None
