from pathlib import Path

import pytest

from pynano.checkers import SyntaxChecker
from pynano.pyn import PyNano


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
        Path(__file__).resolve() / "examples" / "empty.pyn",
        Path(__file__).resolve() / "examples" / "demo_func.pyn",
    ),
)
def pytest_pynano_example(pynano, program):
    assert pynano.compile(program)
