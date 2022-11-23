""" A tiny tiny cpu RISC-V emulator """

import glob
from elftools.elf.elffile import ELFFile


#CONSTANTS
PC = 32 
MEMORY = b'\x00'*0x4000 #(one kibibyte)




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
        for segment in elf.iter_segments():
            print(segment.header.get("p_paddr"))

if __name__ == "__main__":
    for name in glob.iglob("dumps/*"):
        read_elf(name)
