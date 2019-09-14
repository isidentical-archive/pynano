import ast
from enum import IntEnum


class Precedence(IntEnum):
    INITAL = 0
    LOW = 1
    AVG = 2
    HAVG = 3
    FINAL = 4


def parse(node: ast.Name):
    return node.id
