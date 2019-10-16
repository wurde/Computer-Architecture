"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # 256 bytes of memory
        self.ram = [0] * 256
        # Create 8 registers, 1 byte each
        self.reg = [0] * 8

        self.pc = 0
        self.reg[5] = 0 # IM
        self.reg[6] = 0 # IS
        self.reg[7] = 0 # SP
        self.instruction = {
            "NOP":  0b00000000,
            "HLT":  0b00000001,
            "PUSH": 0b01000101,
            "PRN":  0b01000111,
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

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
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
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 2
            elif command == self.instruction['PRN']:
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 1
            elif command == self.instruction['MUL']:
                reg_a = self.reg[self.ram_read(self.pc + 1)]
                reg_b = self.reg[self.ram_read(self.pc + 2)]
                self.reg[self.ram[self.pc + 1]] = reg_a * reg_b
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
