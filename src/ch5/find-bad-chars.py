#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Write a Script to Find Bad Characters in this example
# - More examples:
# - http://www.securitytube.net/groups?operation=view&groupId=7
# - Buffer Overflow
# - SEH

import immlib


def main(args):

    address = int(args[0], 16)
    imm = immlib.Debugger()

    chars = '0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f303132333435363738393a3b3c3d3e3f404142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'

    stack_chars = imm.readMemory(address, len(chars))
    stack_chars = stack_chars.encode('HEX')

    for c, cs in zip(chars, stack_chars):
        imm.log('Stack: %s Shellcode: %s' % (c, cs))
        if c == cs:
            continue
        imm.log('[+] Bad character detected: %s' % c)
        return '[*] Your shellcode contains a bad character: %s' % c

    imm.log('[+] Your shellcode is clean')
    return 'Command executed'
