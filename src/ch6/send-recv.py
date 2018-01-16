#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - For both send/recv can read the arguments from the stack when the breakpoint is hit and print contents out of an intelligible way coherent with the API documentation

from pydbg import *
from pydgb.defines import *
import argparse
import os


def send_bp(dbg):
    print('Send called!')
    print('Data:', dbg.dump_context(dbg.context))
    return DBG_CONTINUE


def recv_bp(dbg):
    print('Recv called!')
    print('Data:', dbg.dump_context(dbg.context))
    return DBG_CONTINUE


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

send_api_address = dbg.func_resolve('ws2_32', 'send')
dbg.bp_set(send_api_address, description='Send Breakpoint', handler=send_bp)

recv_api_address = dbg.func_resolve('ws2_32', 'recv')
dbg.bp_set(recv_api_address, description='Recv Breakpoint', handler=recv_bp)
