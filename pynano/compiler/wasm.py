from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import List, Union

from pynano.compiler import Compiler


@dataclass
class Definition:
    name: str

    def __str__(self):
        return f"${self.name}"


@dataclass(init=False)
class Instruction:
    name: str
    parameters: List[Union[str, Instruction]] = field(default_factory=list)

    def __init__(self, name, *parameters):
        self.name = name
        self.parameters = list(parameters)

    def __str__(self):
        base = f"({self.name}"
        for parameter in self.parameters:
            base += f" {parameter}"
        base += ")"
        return base


class WASMTypes:
    TYPES = {"integer": "i32"}

    def __class_getitem__(cls, attr):
        return cls.TYPES.get(attr.id)


class WASMCompiler(Compiler):
    def visit_Module(self, node):
        module = Instruction("module")
        for child in node.body:
            child = self.visit(child)
            if isinstance(child, Instruction):
                module.parameters.append(child)
        return module

    def visit_FunctionDef(self, node):
        function = Instruction("func")
        for arg in node.args.args:
            name = Definition(arg.arg)
            arg_type = WASMTypes[arg.annotation]
            function.parameters.append(Instruction("param", name, arg_type))
        function.parameters.append(Instruction("result", WASMTypes[node.returns]))
        return function
