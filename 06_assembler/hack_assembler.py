#!/usr/bin/python3

import sys
from parser import Parser

in_file_assembly = sys.argv[1]
assert '.asm' in in_file_assembly

psr = Parser(in_file_assembly)
psr.parse()
