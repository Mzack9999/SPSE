# Author: SPSE-3232
# Purpose:
# - Our vulnerable program uses strcpy()
# - Can you create a hook for the strcpy() function which will print all the function arguments
# - How can we infer an overflow is about it happen?

import immlib
from immlib import BpHook


class StrcpyHook(BpHook):

    def __init__(self):
        BpHook.__init__(self)

    def run(self, registers):
        imm = immlib.Debugger()
        imm.log('[+] strcpy called')

        eip = registers['ESP']
        arg1 = registers['ECX']
        arg2 = registers['EAX']

        imm.log('[+] EIP: 0x%08x ARG1: 0x%08x ARG2: 0x%08x' % (eip, arg1, arg2))

        source_string = imm.readString(arg1)
        destination_string = imm.readString(arg2)

        imm.log('[+] destination_string: %s' % destination_string)

        if len(source_string) > len(destination_string):
            imm.log('[+] Possible buffer overflow detected!')


def main(args):
    imm = immlib.Debugger()

    function_name = 'strcpy'
    function_address = imm.getAddress(function_name)

    hook = StrcpyHook()
    hook.add(function_name, function_address)

    imm.log('[+] Hook for the function %s installed' % function_name)

    return 'StrcpyHook installed!'
