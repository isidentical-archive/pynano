import argparse
from pathlib import Path
from unittest import mock

from pynano.__main__ import main, parse_args
from pynano.compiler import WASMCompiler

BASE_PATH = Path(__file__).parent.resolve()


@mock.patch(
    "argparse.ArgumentParser.parse_args",
    return_value=argparse.Namespace(
        file=BASE_PATH / "examples" / "empty.pyn", backend=WASMCompiler()
    ),
)
def test_cmdline(_, capsys):
    main(**vars(parse_args()))
    out, _ = capsys.readouterr()
    assert out == "(module)\n"
