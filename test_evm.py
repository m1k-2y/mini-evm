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

def test_add_stack_underflow_zero_element():

    bytecode = bytes.fromhex("0100")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(RuntimeError, match="Stack Underflow"):
        test_evm.run()
        
def test_add_stack_underflow_one_element():

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

def test_mul():

    bytecode = bytes.fromhex("600560030200")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [15]

    assert test_evm.pc == 5

def test_mul_zero():

    bytecode = bytes.fromhex("600560000200")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [0]

def test_mul_stack_underflow():

    bytecode = bytes.fromhex("60050200")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(RuntimeError, match="Stack Underflow"):
        test_evm.run()

def test_mul_overflow():

    bytecode = bytes.fromhex("0200")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.stack = [2 ** 255, 2]

    test_evm.run()

    assert test_evm.stack == [0]

def test_sub():

    bytecode = bytes.fromhex("600360050300")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [2]

    assert test_evm.pc == 5

def test_sub_stack_underflow():

    bytecode = bytes.fromhex("60050300")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(RuntimeError, match="Stack Underflow"):
        test_evm.run()

def test_sub_overflow():

    bytecode = bytes.fromhex("600560030300")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [2 ** 256 -2]

def test_div():

    bytecode = bytes.fromhex("6002600A0400")
    
    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [5]

    assert test_evm.pc == 5

def test_round_down():

    bytecode = bytes.fromhex("600260070400")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [3]

    assert test_evm.pc == 5

def test_zero_division():

    bytecode = bytes.fromhex("600060100400")

    test_evm = MINIEVM(bytecode, 100000)

    test_evm.run()

    assert test_evm.stack == [0]

    assert test_evm.pc == 5

def test_div_stack_underflow():

    bytecode = bytes.fromhex("60100400")

    test_evm = MINIEVM(bytecode, 100000)

    with pytest.raises(RuntimeError, match="Stack Underflow"):
        test_evm.run()
