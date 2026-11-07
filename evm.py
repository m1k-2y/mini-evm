class MINIEVM:
    def __init__(self, bytecode, gas_limit):

        self.code = bytecode
        self.pc = 0
        self.stack = []
        self.gas_remaining = gas_limit
        self.storage = {}
        self.halted = False

    def PUSH1(self):

        self.pc += 1

        if (self.pc == len(self.code)):
            self.stack.append(0)

        else:
            self.stack.append(self.code[self.pc])

        self.pc += 1

    def STOP(self):

        self.halted = True

    def ADD(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")
        
        else:
            value = self.stack.pop()
            value = (value + self.stack.pop()) % 2**256

            self.stack.append(value)

            self.pc += 1

    def step(self):

        if (self.pc >= len(self.code)):
            self.halted = True

        else:
            if (self.code[self.pc] == 0x60):
               self.PUSH1()

            elif (self.code[self.pc] == 0x00):
                self.STOP()

            elif (self.code[self.pc] == 0x01):
                self.ADD()

            else:
                raise ValueError("Unsupported Opcode")
    
    def run(self):

        while not (self.halted):
            self.step()
