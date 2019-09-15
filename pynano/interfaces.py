import ast
from enum import IntEnum
from typing import Optional


class Precedence(IntEnum):
    INITAL = 0
    LOW = 1
    AVG = 2
    HAVG = 3
    FINAL = 4


def parse(node: Optional[ast.expr]) -> str:  # type: ignore
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Constant) and node.value is None:
        return None
