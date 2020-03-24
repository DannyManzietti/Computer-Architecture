"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # memory
        self.ram = [0] * 256
        # regs
        self.reg = [0] * 8
        self.PC = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            ir = self.PC
            # read
            op = self.ram_read(ir)
            # read operands
            operand_a = self.ram_read(ir + 1)
            operand_b = self.ram_read(ir + 2)

            # execute
            if op == HLT:
                # stop
                break
            elif op == LDI:
                # set value to int
                self.reg[operand_a] = operand_b
            elif op == PRN:
                # print value stored in register
                print(self.reg[operand_a])
            else:
                print(f"Commant not found: {bin(op)}")

            # check to see command sets pc
            # update pc if it doesnt
            if op & 16 == 0:
                num_operands = 0
                if op & 64 != 0:
                    num_operands += 1
                elif op & 128 != 0:
                    num_operands += 2
                self.PC += num_operands + 1

    def ram_read(self, mar):
        "Return Value Stored"
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mar, mdr):
        "Write Value"
        self.ram[mar] = mdr
