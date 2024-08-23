from keystone import *
from itertools import islice
import argparse
import os
import sys


HEX = "0123456789abcdef"
NSOBID = "3CA12DFAAF9C82DA064D1698DF79CDA1"
BASE_OFFSET = 0x100 # NSO header is 0x100 bytes in size


def sym_resolver(symbol, value):
    raise NotImplementedError("symbol resolver")
    return False


def assemble(code: bytes, address: int) -> list[bytes]:
    ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
    ks.sym_resolver = sym_resolver
    encoding, count = ks.asm(code, address)
    return [encoding[i:i+4] for i in range(0, count*4, 4)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input .asm file")
    parser.add_argument("outdir", help="directory to be created with .ips file inside")

    args = parser.parse_args()

    with open(args.infile, "r") as f:
        lines = [line.split(";")[0].rstrip() for line in f.readlines()]

    os.mkdir(args.outdir)

    patches = []
    address = None

    for i, line in enumerate(lines):
        if line == "":
            pass

        elif line.startswith(" ") or line.startswith("\t"):
            if address is None:
                print(f"error: missing address before patch on line {i+1}", file=sys.stderr)
                sys.exit(1)

            patch.append(line.lstrip())

        elif len(line) == 9 and line[-1] == ":" and all(c.lower() in HEX for c in line[:-1]):
            if address is not None:
                patches.append((address, ";".join(patch)))

            address = int(line[:-1], 16)
            patch = []

        else:
            print(f"error: invalid line on line {i+1}", file=sys.stderr)
            sys.exit(1)

    if address is not None:
        patches.append((address, ";".join(patch)))



    with open(f"{args.outdir}/{NSOBID}.ips", "wb") as f:
        f.write(b"IPS32")

        for address, code in patches:
            opcodes = assemble(code, address)

            for i, opcode in enumerate(opcodes):
                f.write((BASE_OFFSET + address + 4*i).to_bytes(4, "big"))
                f.write(b"\x00\x04")
                f.write(bytes(list(opcode)))
            
        f.write(b"EEOF")

if __name__ == '__main__':
    main()
