#!/usr/bin/python3

import sys
from parser import Parser

in_file_assembly = sys.argv[1]
assert '.asm' in in_file_assembly
out_file_binary = in_file_assembly.replace('asm', 'hack')

psr = Parser(in_file_assembly)
psr.parse()
