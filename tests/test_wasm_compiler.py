import ast

import pytest

from pynano.compiler import WASMCompiler
from pynano.compiler.wasm import (
    WASM_TYPES,
    Definition,
    Instruction,
    WASMCompilationError,
)


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


def test_wasm_functiondef_return_none(compiler):
    astfuncdef = ast.parse("def __test(a: integer, b: integer) -> None: pass")
    resfuncdef = compiler.compile(astfuncdef)
    assert resfuncdef == Instruction(
        "module",
        Instruction(
            "func",
            Instruction("param", Definition("a"), WASM_TYPES["integer"]),
            Instruction("param", Definition("b"), WASM_TYPES["integer"]),
        ),
    )


@pytest.mark.parametrize(
    "cpack", [("integer", 13), ("float", 0.5), ("float", 1.2), ("integer", 10 ** 5)]
)
def test_wasm_compiler_valid_constant(compiler, cpack):
    constant_type, constant = cpack
    astconstantdef = ast.parse(str(constant), "<test>", "eval").body
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == Instruction(f"{WASM_TYPES[constant_type]}.const", constant)


def test_wasm_compiler_invalid_constant(compiler):
    astconstantdef = ast.parse("'pynano'", "<test>", "eval").body
    with pytest.raises(WASMCompilationError) as compilation_error:
        compiler.compile(astconstantdef)

    compilation_error = compilation_error.value
    assert compilation_error.msg.startswith("Unknown type str")
