import ast

import pytest

from pynano.compiler import WASMCompiler
from pynano.compiler.wasm import WASM_TYPES, Definition, Instruction


@pytest.fixture
def compiler():
    return WASMCompiler()


def test_definition():
    defx = Definition("x")
    assert defx.name == "x"
    assert str(defx) == "$x"


def test_instruction():
    instr = Instruction("test")
    assert instr.name == "test"
    assert instr.parameters == []
    assert str(instr) == "(test)"


def test_instruction_complex():
    instr = Instruction("test")
    instr.parameters.append("bla")
    instr.parameters.append(Definition("bla"))
    assert str(instr) == "(test bla $bla)"

    subinstr = Instruction("bla")
    instr.parameters.append(subinstr)
    assert str(instr) == "(test bla $bla (bla))"

    instr.parameters.append(subinstr)
    assert str(instr) == "(test bla $bla (bla) (bla))"


def test_wasm_module(compiler):
    assert compiler.compile(ast.Module([])) == Instruction("module")


@pytest.mark.parametrize(
    "types", (["integer", "integer", "integer"], ["float", "integer", "float"])
)
def test_wasm_functiondef(compiler, types):
    astfuncdef = ast.parse("def __test(a: {}, b: {}) -> {}: pass".format(*types))
    resfuncdef = compiler.compile(astfuncdef)
    assert resfuncdef == Instruction(
        "module",
        Instruction(
            "func",
            Instruction("param", Definition("a"), WASM_TYPES[types[0]]),
            Instruction("param", Definition("b"), WASM_TYPES[types[1]]),
            Instruction("result", WASM_TYPES[types[2]]),
        ),
    )
