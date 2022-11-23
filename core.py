from elftools.elf.elffile import ELFFile
import glob

# RISC-V tiny tiny core
"""
Reads_elf_files

Args:
    filepath to elf file
"""

def read_elf(filepath):
    with open(filepath, 'rb') as f:
        e = ELFFile(f)
        for x in e.iter_segments():
            print(x.header.get("p_paddr"))



if __name__ == "__main__":
    for name in glob.iglob('dumps/*'):
        read_elf(name)
    
