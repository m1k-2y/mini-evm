class MINIEVM:
    def __init__(self, bytecode, gas_limit):

        self.code = bytecode
        self.pc = 0
        self.stack = []
        self.gas_remaining = gas_limit
        self.memory = bytearray()
        self.storage = {}
        self.halted = False

    def consume_gas(self, cost):

        if (self.gas_remaining - cost < 0):
            raise RuntimeError("Out of Gas")

        else:
            self.gas_remaining -= cost
        
    def PUSH(self, value):

        if (len(self.stack) >= 1024):
            raise RuntimeError("Stack Overflow")

        else:
            self.stack.append(value)
        
    def PUSH1(self):

        self.pc += 1

        if (self.pc == len(self.code)):
            self.PUSH(0)

        else:
            self.PUSH(self.code[self.pc])

        self.pc += 1

    def STOP(self):

        self.halted = True

    def ADD(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")
        
        else:
            value = self.stack.pop()
            value = (value + self.stack.pop()) % (2 ** 256)

            self.PUSH(value)

            self.pc += 1

    def MUL(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack.pop()
            value = (value * self.stack.pop()) % (2 ** 256)

            self.PUSH(value)

            self.pc += 1

    def SUB(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack.pop()
            value = (value - self.stack.pop()) % (2 ** 256)

            self.PUSH(value)

            self.pc += 1

    def DIV(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value2 == 0):
                self.PUSH(0)

            else:
                value = int(value1 / value2)

                self.PUSH(value)

            self.pc += 1

    def POP(self):

        if (len(self.stack) == 0):
            raise RuntimeError("Stack Underflow")

        else:
            self.stack.pop()

            self.pc += 1

    def DUP1(self):

        if (len(self.stack) == 0):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack[len(self.stack) - 1]

            self.PUSH(value)

            self.pc += 1

    def SWAP1(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            self.PUSH(value1)
            self.PUSH(value2)

            self.pc += 1            

    def LT(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value2 > value1):
                self.PUSH(1)

            else:
                self.PUSH(0)

            self.pc += 1

    def GT(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value1 > value2):
                self.PUSH(1)

            else:
                self.PUSH(0)

            self.pc += 1

    def EQ(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value1 == value2):
                self.PUSH(1)

            else:
                self.PUSH(0)

            self.pc += 1

    def ISZERO(self):

        if (len(self.stack) == 0):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack.pop()

            if (value == 0):
                self.PUSH(1)

            else:
                self.PUSH(0)

            self.pc += 1

    def AND(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            value = value1 & value2

            self.PUSH(value)

            self.pc += 1

    def OR(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            value = value1 | value2

            self.PUSH(value)

            self.pc += 1

    def NOT(self):

        if (len(self.stack) == 0):
            raise RuntimeError("Stack Underflow")

        else:
            mask = (2 ** 256 - 1)

            value = self.stack.pop()

            value = ~(value) & mask

            self.PUSH(value)

            self.pc += 1

    def MLOAD(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            payload = self.stack.pop()

            value = self.stack.pop()

            memory_len = len(self.memory)

            if (memory_len - 1 < payload + 31):
                self.memory.extend(bytearray(payload - memory_len + 32))

            
                                   
            
            
    def step(self):

        if (self.pc >= len(self.code)):
            self.halted = True

        else:
            if (self.code[self.pc] == 0x60):
                self.consume_gas(3)
                self.PUSH1()

            elif (self.code[self.pc] == 0x00):
                self.consume_gas(0)
                self.STOP()

            elif (self.code[self.pc] == 0x01):
                self.consume_gas(3)
                self.ADD()

            elif (self.code[self.pc] == 0x02):
                self.consume_gas(5)
                self.MUL()

            elif (self.code[self.pc] == 0x03):
                self.consume_gas(3)
                self.SUB()

            elif (self.code[self.pc] == 0x04):
                self.consume_gas(5)
                self.DIV()

            elif (self.code[self.pc] == 0x50):
                self.consume_gas(2)
                self.POP()

            elif (self.code[self.pc] == 0x80):
                self.consume_gas(3)
                self.DUP1()

            elif (self.code[self.pc] == 0x90):
                self.consume_gas(3)
                self.SWAP1()

            elif (self.code[self.pc] == 0x10):
                self.consume_gas(3)
                self.LT()

            elif (self.code[self.pc] == 0x11):
                self.consume_gas(3)
                self.GT()

            elif (self.code[self.pc] == 0x14):
                self.consume_gas(3)
                self.EQ()

            elif (self.code[self.pc] == 0x15):
                self.consume_gas(3)
                self.ISZERO()

            elif (self.code[self.pc] == 0x16):
                self.consume_gas(3)
                self.AND()

            elif (self.code[self.pc] == 0x17):
                self.consume_gas(3)
                self.OR()

            elif (self.code[self.pc] == 0x19):
                self.consume_gas(3)
                self.NOT()
                
            else:
                raise ValueError("Unsupported Opcode")
    
    def run(self):

        while not (self.halted):
            self.step()
