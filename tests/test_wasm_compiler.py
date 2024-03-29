import ast

import pytest

from pynano.compiler import WASMCompiler
from pynano.compiler.wasm import (
    WASM_PY_TYPES,
    WASM_TYPES,
    Definition,
    Instruction,
    SubInstruction,
    WASMCompilationError,
)
from pynano.interfaces import NanoSymbolError, Scopes


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

    tempinstr = Instruction("bla")
    instr.parameters.append(tempinstr)
    assert str(instr) == "(test bla $bla (bla))"

    instr.parameters.append(tempinstr)
    assert str(instr) == "(test bla $bla (bla) (bla))"


def test_subinstruction_complex():
    instr = SubInstruction("test")
    instr.parameters.append("bla")
    instr.parameters.append(Definition("bla"))
    assert str(instr) == "test bla $bla"

    tempinstr = Instruction("bla")
    instr.parameters.append(tempinstr)
    assert str(instr) == "test bla $bla (bla)"

    instr.parameters.append(SubInstruction("bla"))
    assert str(instr) == "test bla $bla (bla) bla"


def test_wasm_module(compiler):
    assert compiler.compile(ast.Module([])) == Instruction("module")


@pytest.mark.parametrize(
    "types", (["integer", "integer", "integer"], ["float", "integer", "float"])
)
def test_wasm_functiondef(compiler, types):
    astfuncdef = ast.parse(
        "def __test(a: {}, b: {}) -> {}: pass".format(*types)
    )
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


def test_wasm_compiler_expr_inlining(compiler):
    astconstantdef = ast.parse("1", "<test>", "eval").body  # body => Constant
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == compiler.compile(ast.parse("1", "<test>", "eval"))


@pytest.mark.parametrize(
    "cpack",
    [("integer", 13), ("float", 0.5), ("float", 1.2), ("integer", 10 ** 5)],
)
def test_wasm_compiler_valid_constant(compiler, cpack):
    constant_type, constant = cpack
    astconstantdef = ast.parse(str(constant), "<test>", "eval").body
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == SubInstruction(
        f"{WASM_TYPES[constant_type]}.const", constant
    )


def test_wasm_compiler_invalid_constant(compiler):
    astconstantdef = ast.parse("'pynano'", "<test>", "eval").body
    with pytest.raises(WASMCompilationError) as compilation_error:
        compiler.compile(astconstantdef)

    compilation_error = compilation_error.value
    assert compilation_error.msg.startswith("Unknown type str")


def test_wasm_compiler_module_name(compiler):
    compiler._symbol_table.module[Definition("a")] = 1
    astnamedef = ast.parse("a", "<test>", "eval").body
    resnamedef = compiler.compile(astnamedef)
    assert resnamedef == SubInstruction("global.get", Definition("a"))


def test_wasm_compiler_local_name(compiler):
    compiler._symbol_table.local[Definition("a")] = 1
    compiler._scope = Scopes.LOCAL
    astnamedef = ast.parse("a", "<test>", "eval").body
    resnamedef = compiler.compile(astnamedef)
    assert resnamedef == SubInstruction("local.get", Definition("a"))


def test_wasm_compiler_name_precedence(compiler):
    compiler._symbol_table.local[Definition("a")] = 1
    compiler._symbol_table.module[Definition("a")] = 1
    compiler._scope = Scopes.LOCAL
    astnamedef = ast.parse("a", "<test>", "eval").body
    resnamedef = compiler.compile(astnamedef)
    assert resnamedef == SubInstruction("local.get", Definition("a"))


def test_wasm_compiler_name_not_exist(compiler):
    astnamedef = ast.parse("a", "<test>", "eval").body
    with pytest.raises(NanoSymbolError) as symbol_error:
        compiler.compile(astnamedef)

    symbol_error = symbol_error.value
    assert symbol_error.msg.startswith(f"Couldn't find {Definition('a')}")


def test_wasm_compiler_module_scope_local_name(compiler):
    compiler._symbol_table.local[Definition("a")] = 1
    astnamedef = ast.parse("a", "<test>", "eval").body
    with pytest.raises(NanoSymbolError) as symbol_error:
        compiler.compile(astnamedef)

    symbol_error = symbol_error.value
    assert symbol_error.msg.startswith(f"Couldn't find {Definition('a')}")


OP_TYPES = {"+": "add", "-": "sub", "*": "mul", "/": "div"}


@pytest.mark.parametrize(
    "cpack", [(1, 2), (0.2, 0.5), (3.2, 3.7), (10 ** 4, 10 ** 5)]
)
@pytest.mark.parametrize("operator", "+-*/")
def test_wasm_compiler_binop(compiler, cpack, operator):
    left, right = cpack
    astconstantdef = ast.parse(
        f"{left} {operator} {right}", "<test>", "eval"
    ).body
    resconstantdef = compiler.compile(astconstantdef)
    left_type = WASM_PY_TYPES[type(left)]
    assert resconstantdef == [
        SubInstruction(f"{left_type}.const", left),
        SubInstruction(f"{left_type}.const", right),
        SubInstruction(f"{left_type}.{OP_TYPES[operator]}"),
    ]


def test_wasm_compiler_binop_local_local(compiler):
    compiler._symbol_table.local[Definition("a")] = 1
    compiler._symbol_table.local[Definition("b")] = 1
    compiler._scope = Scopes.LOCAL
    astconstantdef = ast.parse(f"a + b", "<test>", "eval").body
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == [
        SubInstruction(f"local.get", Definition("a")),
        SubInstruction(f"local.get", Definition("b")),
        SubInstruction(f"i32.add"),
    ]


def test_wasm_compiler_binop_local_module(compiler):
    compiler._symbol_table.local[Definition("a")] = 1
    compiler._symbol_table.module[Definition("b")] = 1
    compiler._scope = Scopes.LOCAL
    astconstantdef = ast.parse(f"a + b", "<test>", "eval").body
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == [
        SubInstruction(f"local.get", Definition("a")),
        SubInstruction(f"global.get", Definition("b")),
        SubInstruction(f"i32.add"),
    ]


def test_wasm_compiler_binop_module_module(compiler):
    compiler._symbol_table.module[Definition("a")] = 1
    compiler._symbol_table.module[Definition("b")] = 1
    compiler._scope = Scopes.LOCAL
    astconstantdef = ast.parse(f"a + b", "<test>", "eval").body
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == [
        SubInstruction(f"global.get", Definition("a")),
        SubInstruction(f"global.get", Definition("b")),
        SubInstruction(f"i32.add"),
    ]


def test_wasm_compiler_binop_local_const(compiler):
    compiler._symbol_table.local[Definition("a")] = 1.0
    compiler._scope = Scopes.LOCAL
    astconstantdef = ast.parse(f"1 + a", "<test>", "eval").body
    resconstantdef = compiler.compile(astconstantdef)
    assert resconstantdef == [
        SubInstruction(f"i32.const", 1),
        SubInstruction(f"local.get", Definition("a")),
        SubInstruction(f"f32.add"),
    ]
