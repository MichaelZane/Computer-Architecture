"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self, pc=0, running=True):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = pc 
        self.ram = [0] * 255
        self.running = running
        
        self.branch_table = {}
        self.branch_table[LDI] = self.LDI        
        self.branch_table[PRN] = self.PRN
        self.branch_table[HLT] = self.HLT
        self.branch_table[MUL] = self.MUL
    """
    The instruction pointed to by the PC is 
    fetched from RAM, decoded, and executed.
    """
    
    
    def ram_read(self, MAR):
        return self.ram[MAR] #set the value to Memory Address Register, holds the memory address we're reading or writing
        

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR #Memory Data Register, holds the value to write or the value just read
    
    def LDI(self, op, r1, r2):
        self.reg[r1] = r2
        self.pc += 3
    
    def PRN(self, op, r1, r2):
        print(self.reg[r1])
        self.pc += 2
    
    def HLT(self, op, r1, r2):
        self.running = False
          
    def MUL(self, op, r1, r2):
        
        self.alu("MUL",r1, r2) 
        self.pc += 3

    def load(self):
        """Load a program into memory."""

        filename = sys.argv[1]
        address = 0
        with open(filename) as f:
            
            for line in f:
                
                line = line.split("#") 
                
                try:
                     
                    val = int(line[0].strip(), 2)
                    
                    
                except ValueError:
                    continue
                
                self.ram_write(address, val)
                address += 1
    


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        
        """
        Run the CPU.      
        """    
        while self.running:
            ir = self.ram_read(self.pc)
            op = ir
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            
            self.branch_table[ir]( op, op_a, op_b)
            
            
       
m = CPU()
m.load()
m.run()              
                