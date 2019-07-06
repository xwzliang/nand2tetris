#!/usr/bin/python3

from sys import argv
from pathlib import Path

from parser import Parser

path_input = Path(argv[1])
assert path_input.exists(), "Path not exists."

if path_input.is_dir():	# Translate all vm files in directory
    vmfiles = [f for f in path_input.glob('*.vm')]
    assert vmfiles, "No vm file in this directory."
    for vmfile in vmfiles:
        psr = Parser(vmfile)
        returned_contents = psr.parse()
else:	# Translate one vm file
    vmfile = path_input
    psr = Parser(vmfile)
    returned_contents = psr.parse()
print(returned_contents)
