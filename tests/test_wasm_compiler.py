from pynano.compiler import WASMCompiler
from pynano.compiler.wasm import Definition, Instruction


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
