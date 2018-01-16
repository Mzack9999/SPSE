#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Modify the program to include full crash dump details. Explore how you can get info using the utils module

from pydbg import *
from pydbg.defines import *
import argparse
import os


def detect_overflow(dbg):
    if dbg.dbg.u.Exception.dwFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED

    print('Access Violation Happened!')
    print('EIP: {eip}'.format(eip=dbg.context.Eip))
    print('Crush dump data:', dbg.dump_context())

    return DBG_EXCEPTION_NOT_HANDLED


parser = argparse.ArgumentParser(description='Crash Dump')
parser.add_argument('-f', '--file', help='file.', required=True)
args = parser.parse_args()

if not os.path.exists(args.file):
    print('File not found!')
    exit(1)

os.system('start "{file}"'.format(file=args.file))

dbg = pydbg()
for (pid, name) in dbg.enumerate_processes():
    if name.lower() == args.file:
        dbg.attach(pid)

dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, detect_overflow)
dbg.run()