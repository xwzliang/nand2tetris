#!/usr/bin/python3

from sys import argv
from pathlib import Path

from parser import Parser
from code_writer import CodeWriter

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
    out_asm_file = path_input.with_suffix('.asm')
    psr = Parser(vmfile)
    returned_contents = psr.parse()
    cw = CodeWriter(returned_contents, out_asm_file)
    cw.write()
# print(returned_contents)
print('Successfully translate to assembly ' + out_asm_file.as_posix())
