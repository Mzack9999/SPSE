#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Take a DLL name as input and check if a given PE imports it and print the list of imports

# Command line args

import argparse
import pefile
import os

parser = argparse.ArgumentParser(description='Dll imports')
parser.add_argument('-p', '--pe', help='pefile.', required=True)
parser.add_argument('-d', '--dll', help='dll.', required=True)
args = parser.parse_args()

if not os.path.exists(args.pe):
    print('Pefile not found!')
    exit(1)

pe = pefile.PE(args.pe)

for entry in pe.DIRECTORY_ENTRY_IMPORT:
    print('Dll name: ', entry.dll)
    if entry.dll == args.dll:
        print('Match found!')


