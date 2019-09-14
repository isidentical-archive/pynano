import ast
import os
import tokenize
from typing import List, Optional, Sequence, Type

from pynano.checkers import CHECKERS, SyntaxChecker

Checkers = Sequence[Type[SyntaxChecker]]


class PyNano:
    def __init__(self, checkers: Optional[Checkers]) -> None:
        self.checkers: List[SyntaxChecker] = []
        self._pre_init(checkers or CHECKERS)

    def _pre_init(self, checkers: Checkers, **options) -> None:
        for checker in checkers:
            self.checkers.append(checker())

    def compile(self, file_path: os.PathLike) -> None:
        file_path = os.fspath(file_path)

        with tokenize.open(file_path) as file:
            content = file.read()

        tree = ast.parse(content)
