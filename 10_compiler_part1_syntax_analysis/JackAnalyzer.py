#!/usr/bin/python3

import argparse
from pathlib import Path

from JackTokenizer import JackTokenizer 

arg_parser = argparse.ArgumentParser(description='Compile the input Jack program into syntax analyzed output')
arg_parser.add_argument('path_input', help='The path for Jack program file *.jack or the directory path which contains *.jack files')
args = arg_parser.parse_args()


path_input = Path(args.path_input)
assert path_input.exists(), "Path does not exist."

if path_input.is_dir():	# Compile all jack files in directory
    jackfiles = [f for f in path_input.glob('*.jack')]
    assert jackfiles, "No jack file in this directory."
    for jackfile in jackfiles:
        out_xml_file = jackfile.with_suffix('.xml')
        out_token_xml_file = jackfile.parent / (jackfile.stem + 'T.xml')
        jack_tokenizer = JackTokenizer(jackfile, out_token_xml_file)
        jack_tokenizer.tokenize()
else:	# Compile one jack file
    jackfile = path_input
    out_xml_file = jackfile.with_suffix('.xml')
    out_token_xml_file = jackfile.parent / (jackfile.stem + 'T.xml')
    jack_tokenizer = JackTokenizer(jackfile, out_token_xml_file)
    jack_tokenizer.tokenize()

print('Done')
