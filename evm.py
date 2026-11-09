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
            value = (value + self.stack.pop()) % (2 ** 256)

            self.stack.append(value)

            self.pc += 1

    def MUL(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack.pop()
            value = (value * self.stack.pop()) % (2 ** 256)

            self.stack.append(value)

            self.pc += 1

    def SUB(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack.pop()
            value = (value - self.stack.pop()) % (2 ** 256)

            self.stack.append(value)

            self.pc += 1

    def DIV(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value2 == 0):
                self.stack.append(0)

            else:
                value = int(value1 / value2)

                self.stack.append(value)

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

            self.stack.append(value)

            self.pc += 1

    def SWAP1(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            self.stack.append(value1)
            self.stack.append(value2)

            self.pc += 1            

    def LT(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value2 > value1):
                self.stack.append(1)

            else:
                self.stack.append(0)

            self.pc += 1

    def GT(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value1 > value2):
                self.stack.append(1)

            else:
                self.stack.append(0)

            self.pc += 1

    def EQ(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            if (value1 == value2):
                self.stack.append(1)

            else:
                self.stack.append(0)

            self.pc += 1

    def ISZERO(self):

        if (len(self.stack) == 0):
            raise RuntimeError("Stack Underflow")

        else:
            value = self.stack.pop()

            if (value == 0):
                self.stack.append(1)

            else:
                self.stack.append(0)

            self.pc += 1

    def AND(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            value = value1 & value2

            self.stack.append(value)

            self.pc += 1

    def OR(self):

        if (len(self.stack) < 2):
            raise RuntimeError("Stack Underflow")

        else:
            value1 = self.stack.pop()
            value2 = self.stack.pop()

            value = value1 | value2

            self.stack.append(value)

            self.pc += 1

    def NOT(self):

        if (len(self.stack) == 0):
            raise RuntimeError("Stack Underflow")

        else:
            mask = (2 ** 256 - 1)

            value = self.stack.pop()

            value = ~(value) & mask

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

            elif (self.code[self.pc] == 0x02):
                self.MUL()

            elif (self.code[self.pc] == 0x03):
                self.SUB()

            elif (self.code[self.pc] == 0x04):
                self.DIV()

            elif (self.code[self.pc] == 0x50):
                self.POP()

            elif (self.code[self.pc] == 0x80):
                self.DUP1()

            elif (self.code[self.pc] == 0x90):
                self.SWAP1()

            elif (self.code[self.pc] == 0x10):
                self.LT()

            elif (self.code[self.pc] == 0x11):
                self.GT()

            elif (self.code[self.pc] == 0x14):
                self.EQ()

            elif (self.code[self.pc] == 0x15):
                self.ISZERO()

            elif (self.code[self.pc] == 0x16):
                self.AND()

            elif (self.code[self.pc] == 0x17):
                self.OR()

            elif (self.code[self.pc] == 0x19):
                self.NOT()
                
            else:
                raise ValueError("Unsupported Opcode")
    
    def run(self):

        while not (self.halted):
            self.step()
