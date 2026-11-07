from evm import MINIEVM
import pytest

def test_add():

    bytecode = bytes.fromhex("600560030100")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [8]

    assert test_evm.pc == 5
    
def test_push1():

    bytecode = bytes.fromhex("600A00")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [10]

    assert test_evm.pc == 2

def test_stop():

    bytecode = bytes.fromhex("006005")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == []

    assert test_evm.pc == 0

    assert test_evm.halted == True
    
def test_empty_bytecode():

    bytecode = bytes.fromhex("")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == []

    assert test_evm.pc == 0

    assert test_evm.halted == True

def test_stack_underflow_zero_element():

    bytecode = bytes.fromhex("0100")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(RuntimeError, match="Stack Underflow"):
        test_evm.run()
        
def test_stack_underflow_one_element():

    bytecode = bytes.fromhex("60050100")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(RuntimeError, match="Stack Underflow"):
        test_evm.run()
        
def test_unsupported_opcode():

    bytecode = bytes.fromhex("FE00")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(ValueError, match="Unsupported Opcode"):
        test_evm.run()

def test_push1_zero_data():

    bytecode = bytes.fromhex("60")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [0]

    assert test_evm.pc == 2

def test_add_overflow():

    bytecode = bytes.fromhex("0100")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.stack = [2 ** 256 - 1, 1]

    test_evm.run()

    assert test_evm.stack == [0]
