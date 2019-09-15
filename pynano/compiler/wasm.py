from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import List, Union

from pynano.compiler import CompilationError, Compiler, context_change
from pynano.interfaces import NanoSymbolError, Scopes, parse

WASM_TYPES = {"integer": "i32", "float": "f32"}
WASM_PY_TYPES = {int: "i32", float: "f32"}
Parameter = Union[str, "Definition", "Instruction"]


class WASMCompilationError(CompilationError):
    pass


@dataclass(frozen=True, unsafe_hash=True)
class Definition:
    name: str

    def __str__(self) -> str:
        return f"${self.name}"


@dataclass(init=False)
class Instruction:
    name: str
    parameters: List[Parameter]
    origin: str = field(repr=False, compare=False)

    def __init__(self, name: str, *parameters: Parameter, origin=None) -> None:
        self.name = name
        self.parameters = list(parameters)
        self.origin = origin or name

    def __str__(self) -> str:
        base = f"({self.name}"
        for parameter in self.parameters:
            base += f" {parameter}"
        base += ")"
        return base

    def __getattr__(self, attr: str) -> Callable[[Parameter], None]:
        self.name = f"{self.name}.{attr}"
        return self.parameters.append


class SubInstruction(Instruction):
    def __str__(self) -> str:
        base = f"{self.name}"
        for parameter in self.parameters:
            base += f" {parameter}"
        base += ""
        return base


class WASMCompiler(Compiler):
    def visit_Module(self, node: ast.Module) -> Instruction:
        module = Instruction("module")
        for child in node.body:
            child = self.visit(child)
            if isinstance(child, Instruction):
                module.parameters.append(child)
        return module

    @context_change
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Instruction:
        function = Instruction("func")
        for arg in node.args.args:
            name = Definition(arg.arg)
            arg_type = WASM_TYPES[parse(arg.annotation)]
            self._symbol_table.local[name] = arg_type
            function.parameters.append(Instruction("param", name, arg_type))
        if return_type := parse(node.returns):
            function.parameters.append(Instruction("result", WASM_TYPES[return_type]))
        return function

    def visit_Constant(self, node: ast.Constant) -> Instruction:
        constant_type = WASM_PY_TYPES.get(type(node.value))
        if constant_type is None:
            raise WASMCompilationError(
                f"Unknown type {type(node.value).__name__} at constant definition.",
                node,
            )

        constant = SubInstruction(constant_type)
        constant.const(node.value)
        return constant

    def visit_Expression(self, node: ast.Expr) -> Instruction:
        return self.visit(node.body)

    def visit_Name(self, node: ast.Name) -> Instruction:
        var = Definition(parse(node))
        if var in self._symbol_table.local and self._scope is Scopes.LOCAL:
            local = SubInstruction("local")
            local.get(var)
            return local
        elif var in self._symbol_table.module:
            module = SubInstruction("global")
            module.get(var)
            return module
        else:
            raise NanoSymbolError(
                f"Couldn't find {var} in local and module scope.", node
            )

    def visit_BinOp(self, node: ast.BinOp) -> Instruction:
        """ (lhs > rhs) => (module = local > const)"""
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left.origin in {"local", "global"}:
            op_type = self._symbol_table[left.parameters[0]]
        elif right.origin in {"local", "global"}:
            op_type = self._symbol_table[right.parameters[0]]
        else:
            op_type = left.origin

        op_type = SubInstruction(op_type)
        getattr(op_type, type(node.op).__name__.lower()[:3])  # e.g i32.add

        return [left, right, op_type]
