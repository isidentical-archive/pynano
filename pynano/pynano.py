import ast
import os
import tokenize
from typing import Optional, Sequence

from pynano.checkers import CHECKERS, SyntaxChecker


class PyNano:
    def __init__(self, checkers: Optional[Sequence[SyntaxChecker]]) -> None:
        self.checkers = checkers or CHECKERS

    def compile(self, file_path: os.PathLike):
        file_path = os.fspath(file_path)

        with tokenize.open(file_path) as file:
            content = file.read()

        tree = ast.parse(content)
