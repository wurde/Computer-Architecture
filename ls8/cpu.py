"""CPU functionality."""

#
# Dependencies
#

import sys

#
# Constants
#

# Stack pointer is register R7
SP = 7
# Interrupt status is register R6
IS = 6
# Interrupt mask is register R5
IM = 5

#
# Class definition
#

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # Create 8 registers, 1 byte each
        self.reg = [0] * 8

        self.pc = 0
        self.reg[IM] = 0
        self.reg[IS] = 0
        self.reg[SP] = 0xF4
        self.instruction = {
            "NOP":  0b00000000,
            "HLT":  0b00000001,
            "RET":  0b00010001,
            "PUSH": 0b01000101,
            "POP":  0b01000110,
            "CALL": 0b01010000,
            "PRN":  0b01000111,
            "INC":  0b01100101,
            "DEC":  0b01100110,
            "ST":   0b10000100,
            "ADD":  0b10100000,
            "SUB":  0b10100001,
            "LDI":  0b10000010,
            "MUL":  0b10100010,
        }

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            f = open(filename, 'r')
            lines = f.readlines()
            f.close()

            for line in lines:
                # Process comments: Ignore anything after a # symbol
                comment_split = line.split("#")

                # Convert any numbers from binary strings to integers
                num = comment_split[0].strip()
                try:
                    val = int(num, 2)
                except ValueError:
                    continue

                self.ram[address] = val
                address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # bitwise-AND the result with 0xFF
        # to keep values within 0 to 255.

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "INC":
            self.reg[reg_a] += 1
        elif op == "DEC":
            self.reg[reg_a] -= 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            command = self.ram_read(self.pc)

            if command == self.instruction['NOP']:
                next
            elif command == self.instruction['LDI']:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.reg[reg_a] = reg_b
                self.pc += 2
            elif command == self.instruction['PRN']:
                reg_a = self.ram_read(self.pc + 1)
                print(self.reg[reg_a])
                self.pc += 1
            elif command == self.instruction['INC']:
                reg_a = self.ram_read(self.pc + 1)
                self.alu("INC", reg_a, None)
                self.pc += 1
            elif command == self.instruction['DEC']:
                reg_a = self.ram_read(self.pc + 1)
                self.alu("DEC", reg_a, None)
                self.pc += 1
            elif command == self.instruction['ADD']:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("ADD", reg_a, reg_b)
                self.pc += 2
            elif command == self.instruction['SUB']:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("SUB", reg_a, reg_b)
                self.pc += 2
            elif command == self.instruction['MUL']:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.alu("MUL", reg_a, reg_b)
                self.pc += 2
            elif command == self.instruction['PUSH']:
                register = self.ram_read(self.pc + 1)
                val = self.reg[register]
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], val)
                self.pc += 1
            elif command == self.instruction['POP']:
                register = self.ram_read(self.pc + 1)
                val = self.ram_read(self.reg[SP])
                self.reg[register] = val
                self.reg[SP] += 1
                self.pc += 1
            elif command == self.instruction['CALL']:
                reg_a = self.reg[self.ram_read(self.pc + 1)]
                self.reg[SP] -= 1
                self.ram_write(self.reg[SP], self.pc + 2)
                self.pc = reg_a
            elif command == self.instruction['RET']:
                register = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                self.pc = register - 1
            elif command == self.instruction['ST']:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.reg[reg_a] = reg_b
                self.pc += 2
            elif command == self.instruction['HLT']:
                running = False
            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)

            if self.pc >= len(self.ram) - 1:
                self.pc = 0
            else:
                self.pc += 1

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, instruction):
        self.ram[pc] = instruction
