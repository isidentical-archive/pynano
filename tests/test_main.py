import argparse
from pathlib import Path
from unittest import mock

import pytest

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


def test_main_not_found_file():
    with pytest.raises(FileNotFoundError) as file_not_found_error:
        main(Path("blabla"))

    assert file_not_found_error.type is FileNotFoundError
    assert file_not_found_error.match("blabla")
