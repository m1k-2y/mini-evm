from evm import MINIEVM

bytecode_hex = input("Bytecodes : ")

bytecode_hex = bytecode_hex.removeprefix("0x")

bytecode = bytes.fromhex(bytecode_hex)

gas_limit = int(input("Gas_Limit : "))

mini_evm = MINIEVM(bytecode, gas_limit)

mini_evm.run()

print(mini_evm.stack)
