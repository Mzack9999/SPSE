#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - code a program which can read an exe and dump interesting information such as import/exports,
#   disassembly, strings etc.
# - basically a powerful level 1 binary analysis tool before you put the exe into a debugger

import argparse
import pefile
import os
from capstone import *


parser = argparse.ArgumentParser(description='Level 1 Disassembler')
parser.add_argument('-f', '--file', help='exe file.', required=True)
args = parser.parse_args()

if not os.path.exists(args.file):
    print('Exe file not found!')
    exit(1)

pe = pefile.PE(args.file)

# Import/Export
print("Imports")
for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print(entry.dll)
    for imp in entry.imports:
        print(hex(imp.address), imp.name)
print("Exports")
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        print(hex(pe.OPTIONAL_HEADER.ImageBase + exp.address), exp.name, exp.ordinal)

# Fetch the index of the resource directory entry containing the strings
rt_string_idx = [
  entry.id for entry in
  pe.DIRECTORY_ENTRY_RESOURCE.entries].index(pefile.RESOURCE_TYPE['RT_STRING'])

# Get the directory entry
rt_string_directory = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_string_idx]

# For each of the entries (which will each contain a block of 16 strings)
for entry in rt_string_directory.directory.entries:
    # Get the RVA of the string data and
    # size of the string data
    data_rva = entry.directory.entries[0].data.struct.OffsetToData
    size = entry.directory.entries[0].data.struct.Size
    print('Directory entry at RVA', hex(data_rva), 'of size', hex(size))

    # Retrieve the actual data and start processing the strings
    data = pe.get_memory_mapped_image()[data_rva:data_rva+size]
    offset = 0
    while True:
        # Exit once there's no more data to read
        if offset >= size:
            break
        # Fetch the length of the unicode string
        ustr_length = pe.get_word_from_data(data[offset:offset+2], 0)
        offset += 2

        # If the string is empty, skip it
        if ustr_length == 0:
            continue

        # Get the Unicode string
        ustr = pe.get_string_u_at_rva(data_rva+offset, max_length=ustr_length)
        offset += ustr_length * 2
        print('String of length', ustr_length, 'at offset', offset, ':', ustr)

# Disassembler
entry_point_address = pe.OPTIONAL_HEADER.AddressOfEntryPoint
code_section = pe.get_section_by_rva(entry_point_address)

code_dump = code_section.get_data()
code_address = pe.OPTIONAL_HEADER.ImageBase + code_section.VirtualAddress

md = Cs(CS_ARCH_X86, CS_MODE_32)

for i in md.disasm(code_dump, code_address):
    print("0x{a}:\t{m}\t{o}".format(a=i.address, m=i.mnemonic, o=i.op_str))