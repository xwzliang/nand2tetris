#!/usr/bin/python3

import argparse
from pathlib import Path

from parser import Parser
from code_writer import CodeWriter

arg_parser = argparse.ArgumentParser(description='Translate vm code into assembly code')
arg_parser.add_argument('path_input', help='The path for vm file *.vm or the directory path which contains *.vm files')
args = arg_parser.parse_args()


path_input = Path(args.path_input)
assert path_input.exists(), "Path not exists."

if path_input.is_dir():	# Translate all vm files in directory
    vmfiles = [f for f in path_input.glob('*.vm')]
    assert vmfiles, "No vm file in this directory."
    out_asm_file = path_input / (path_input.name + '.asm')	# Out asm file name same as directory name
    returned_contents = {}
    for vmfile in vmfiles:
        psr = Parser(vmfile)
        parse_result = psr.parse()
        returned_contents = {**returned_contents, **parse_result}	# Merge returned results to dict returned_contents
else:	# Translate one vm file
    vmfile = path_input
    out_asm_file = path_input.with_suffix('.asm')
    psr = Parser(vmfile)
    returned_contents = psr.parse()

cw = CodeWriter(returned_contents, out_asm_file)
cw.write()
print('Successfully translate to assembly ' + out_asm_file.as_posix())
