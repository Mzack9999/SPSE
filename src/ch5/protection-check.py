#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - What is DEP, ASLR and SafeSEH?
# - Please write PyCommand scripts to find if modules have the above enabled

import immlib
import struct

DESC = "DEP, ASLR, SafeSEH detection in all modules"

# The DLL can be relocated at load time (ASLR)
IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE = 0x0040
# The image is compatible with data execution prevention (DEP)
IMAGE_DLLCHARACTERISTICS_NX_COMPAT = 0x0100
# The image does not use structured exception handling (SEH)
IMAGE_DLLCHARACTERISTICS_NO_SEH = 0x0400


def toHex(addr):
    # converts an integer address to hex
    return "%08X" % addr


def toHexStr(addr):
    # converts an integer address to a hex string with a leading 0x
    return "0x" + toHex(addr)


def inspect_module(imm, module):
    log_message = """
    [+] Inspecting module: {module}\n
    [+] Version: {version}\n
    [+] Base Address: {base_address}, Size: {size}, Entry Point: {entry_point}\n
    """
    name = module.getName()
    base_address = module.getBaseAddress()
    mbase = toHexStr(base_address)
    size = toHexStr (module.getSize())
    entry_point = toHexStr(module.getEntry())
    version = module.getVersion()
    imm.logLines(log_message.format(module=name, version=version, base_address=mbase, size=size, entry_point=entry_point))

    pe_offset = struct.unpack('<L', imm.readMemory(base_address + 0x3c, 4))[0] # + 60 bytes, read 4 bytes
    pe_base = base_address + pe_offset
    flags = struct.unpack('<H', imm.readMemory(pe_base + 0x5e, 2))[0]
    aslr = (flags & IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE) == 0
    dep = (flags & IMAGE_DLLCHARACTERISTICS_NX_COMPAT) == 0
    protection_str = "dep: {dep}, aslr: {aslr}".format(dep=dep, aslr=aslr)
    if (aslr or dep):
        imm.log("[-] " + protection_str)
    else
        imm.log("[+] " + protection_str, highlight=True)

    functions = imm.getAllFunctions(base_address)
    log_message = "[+] Functions found in module: {nbr}".format(nbr=len(functions))
    for f in functions:
        function_str = "[+] Function: {n}, Start Address: {a}"
        func = imm.getFunction(f)
        log_message += function_str.format(n=func.getName(), a=func.getStart())

    imm.logLines(log_message)

def main(args):
    imm = immlib.Debugger()
    modules = imm.getAllModules()
    for m in modules.values():
        inspect_module(imm, m)

    return 'Analysis complete!'