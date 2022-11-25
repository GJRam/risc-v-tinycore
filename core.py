""" A tiny tiny cpu RISC-V emulator """

import glob
import struct
from enum import Enum
from elftools.elf.elffile import ELFFile


regfile = [0] * 33
PC = 32

# define one MB of memory
memory = bytearray(1024 * 1024)

class OP(Enum):
    """
    Class to hold all the opcodes
    """
    LUI = 0b0110111
    AUIPC = 0b0010111
    JAL = 0b1101111
    JALR = 0b1100111
    BRANCH = 0b1100011
    LOAD = 0b0000011
    STORE = 0b0100011
    OP_IMM = 0b0010011
    OP = 0b0110011
    MISC_MEM = 0b0001111
    SYSTEM = 0b1110011

class Func3(Enum):
    """
    Class to hold all func3 values
    """
    ADD_SUB = 0b000
    SLL = 0b001
    SLT = 0b010
    SLTU = 0b011
    XOR = 0b100
    SRL_SRA = 0b101
    OR = 0b110
    AND = 0b111


def pass_data(data, addr):
    """
    Passes instructions to memory

    Args:
        data: instruction to pass
        addr: address to pass instruction
   """ 
   # Doing this to make sure that the file is being run directly
    global memory
    addr -= 0x08000000
    if addr < 0 or addr > len(memory):  
        return
    memory = memory[:addr] + data + memory[addr + len(data):]

   


def dump():
    """
    Prints out the contents of the register file
    """
    print("PC: 0x{:08x}".format(regfile[PC]))
    
    # print registers on the same line
    for i in range(32):
        print("x{:02d}: 0x{:08x}".format(i, regfile[i]))



def get_bits(ins, start, end):
    """
    Gets bits from instruction

    Args:
        ins: instruction
        start: start bit
        end: end bit
    """
    #How this works:
    # 1. Shift the instruction to the right by the start bit
    # 2. Subtract 1 from the end bit
    # 3. Shift the result to the left by the result of step 2
    # 4. Subtract the result of step 3 from the result of step 1
    return (ins >> start) & ((1 << (end - start + 1)) - 1)

def fetch(addr):
    """
    Fetches instruction from memory

    Args:
        regfile[PC]: address to fetch instruction from

    Returns:
        instruction
    """
    addr -= 0x08000000

    if addr < 0 or addr > len(memory):
        raise Exception("Invalid address: 0x{:08x}".format(addr))

    return struct.unpack("<I", memory[addr : addr + 4])[0]


def pipeline_steps():
    #fetch
    ins = fetch(regfile[PC])
    #decode 
    dump()

    #TODO implement the rest of the pipeline
    opcode = get_bits(ins, 0, 7)

    if opcode == OP.JAL:
        print("JAL")
    if opcode == OP.LUI:
        rd = get_bits(ins, 7, 12)
        imm = get_bits(ins, 12, 32) << 12
        regfile[rd] = imm
        regfile[PC] += 4
    elif opcode == OP.AUIPC:  
        pass

    return False

def read_elf(filepath):
    """
    Reads filepath at filepath and returns an ELFFile object

    Args:
        filepath: path to elf file

    Returns:
        None
    """
    with open(filepath, "rb") as file:
        elf = ELFFile(file)
        for seg in elf.iter_segments():
            pass_data(seg.data(), seg.header.p_paddr) 
        regfile[PC] = 0x08000000
        while pipeline_steps():
            pass


if __name__ == "__main__":
    for name in glob.iglob("./dumps/*"):
        print(f"testing {name}")
        read_elf(name)
