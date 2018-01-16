#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a simple program which can disassemble the first 200 bytes of executable code
#
# NB: pydasm is deprecated, using capstone instead

import argparse
import pefile
import os
from capstone import *

parser = argparse.ArgumentParser(description='Capstone disassembler')
parser.add_argument('-f', '--file', help='pefile.', required=True)
args = parser.parse_args()

if not os.path.exists(args.file):
    print('Pefile not found!')
    exit(1)

pe = pefile.PE(args.file)

entry_point_address = pe.OPTIONAL_HEADER.AddressOfEntryPoint
code_section = pe.get_section_by_rva(entry_point_address)

code_dump = code_section.get_data()
code_address = pe.OPTIONAL_HEADER.ImageBase + code_section.VirtualAddress

md = Cs(CS_ARCH_X86, CS_MODE_32)

for i in md.disasm(code_dump, code_address):
    print("0x{a}:\t{m}\t{o}".format(a=i.address, m=i.mnemonic, o=i.op_str))