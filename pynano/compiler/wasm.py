from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import List, Union

from pynano.compiler import Compiler
from pynano.interfaces import parse

WASM_TYPES = {"integer": "i32", "float": "f32"}
Parameter = Union[str, "Definition", "Instruction"]


@dataclass
class Definition:
    name: str

    def __str__(self) -> str:
        return f"${self.name}"


@dataclass(init=False)
class Instruction:
    name: str
    parameters: List[Parameter]

    def __init__(self, name: str, *parameters: Parameter) -> None:
        self.name = name
        self.parameters = list(parameters)

    def __str__(self) -> str:
        base = f"({self.name}"
        for parameter in self.parameters:
            base += f" {parameter}"
        base += ")"
        return base


class WASMCompiler(Compiler):
    def visit_Module(self, node: ast.Module) -> Instruction:
        module = Instruction("module")
        for child in node.body:
            child = self.visit(child)
            if isinstance(child, Instruction):
                module.parameters.append(child)
        return module

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Instruction:
        function = Instruction("func")
        for arg in node.args.args:
            name = Definition(arg.arg)
            arg_type = WASM_TYPES[parse(arg.annotation)]
            function.parameters.append(Instruction("param", name, arg_type))
        if return_type := parse(node.returns):
            function.parameters.append(Instruction("result", WASM_TYPES[return_type]))
        return function
