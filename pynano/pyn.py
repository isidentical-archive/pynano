import ast
import os
import tokenize
from typing import Any, Dict, List, Optional, Sequence, Type

from pynano.checkers import CHECKERS, SyntaxChecker
from pynano.compiler import Compiler, WASMCompiler

Checkers = Sequence[Type[SyntaxChecker]]


class PyNano:
    def __init__(self, checkers: Optional[Checkers] = None) -> None:
        self.checkers: List[SyntaxChecker] = []
        self._pre_init(checkers or CHECKERS)

    def _pre_init(self, checkers: Checkers, **options: Dict[str, Any]) -> None:
        for checker in checkers:
            self.checkers.append(checker())

    def compile(
        self, file_path: os.PathLike, *, backend: Optional[Compiler] = None
    ) -> str:
        file_path = os.fspath(file_path)

        with tokenize.open(file_path) as file:
            content = file.read()

        tree = ast.parse(content)
        for checker in self.checkers:
            checker.check(tree)

        if backend is None:
            backend = WASMCompiler()

        result = backend.compile(tree)
        return result
