#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a Python script which allows you to inspect the “bind” network call and logs the port and IP address used
# - Can be standalone or a Plugin
# - Works on Windows

import immlib
from immlib import BpHook


class BindHook(BpHook):

    def __init__(self):
        BpHook.__init__(self)

    def run(self, registers):
        imm = immlib.Debugger()
        imm.log('[+] bind called')

        eip = registers['ESP']
        # Read sockaddr structure address
        sockaddr = imm.readLong(registers['ESP'] + 8)

        # Read 2 bytes of sin_family member
        sockaddr_sin_family = imm.readShort(sockaddr)

        # Read 2 bytes of sin_port and calculate port number
        # since it is stored as big-endian
        port_hi_byte = ord(imm.readMemory(sockaddr + 2, 1))
        port_low_byte = ord(imm.readMemory(sockaddr + 3, 1))
        sockaddr_sin_port = port_hi_byte * 256 + port_low_byte

        # Read 4 bytes of sin_addr since it is stored as big-endian
        ip_first_byte = ord(imm.readMemory(sockaddr + 4, 1))
        ip_second_byte = ord(imm.readMemory(sockaddr + 5, 1))
        ip_third_byte = ord(imm.readMemory(sockaddr + 6, 1))
        ip_forth_byte = ord(imm.readMemory(sockaddr + 7, 1))

        # Print results to Log View window
        imm.log('---> Pointer to sockaddr structure: 0x%08x' % sockaddr)
        imm.log('---> sockaddr.sin_family: %d' % sockaddr_sin_family)
        imm.log('---> sockaddr.sin_port: %d' % sockaddr_sin_port)
        imm.log('---> sockaddr.sin_addr: %d.%d.%d.%d' %
                (ip_first_byte, ip_second_byte, ip_third_byte, ip_forth_byte))
        imm.log('')
        imm.log("Press F9 to resume")


def main():
    imm = immlib.Debugger()

    function_name = 'bind'
    function_address = imm.getAddress(function_name)

    hook = BindHook()
    hook.add(function_name, function_address)

    imm.log('[+] Hook for the function %s installed' % function_name)

    return 'BindHook installed!'
