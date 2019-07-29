#!/usr/bin/python3

import unittest
from pathlib import Path
import subprocess as sp

class JackAnalyzer(unittest.TestCase):

    def setUp(self):
        self.cwd = Path.cwd()
        self.given_compare_tool = self.cwd.parent / 'tools/TextComparer.sh'
        self.my_jack_analyzer = self.cwd / 'JackAnalyzer.py'

    def compare_output_file(self, jackfile):
        out_xml_file = jackfile.with_suffix('.xml')
        out_token_xml_file = jackfile.parent / (jackfile.stem + 'T.xml')
        cmp_xml_file = out_xml_file.parent / 'given_cmp_file' / out_xml_file.name
        cmp_token_xml_file = out_token_xml_file.parent / 'given_cmp_file' / out_token_xml_file.name
        self.assertTrue(out_token_xml_file.exists())
        # Compare for out_token_xml_file
        proc_compare_token_xml = sp.run([self.given_compare_tool.as_posix(), out_token_xml_file, cmp_token_xml_file], stdout=sp.PIPE, universal_newlines=True)
        self.assertEqual(proc_compare_token_xml.stdout, 'Comparison ended successfully\n')
        # Compare for out_xml_file
        print('Comparing {} and {}'.format(out_xml_file, cmp_xml_file))
        proc_compare_xml = sp.run([self.given_compare_tool.as_posix(), out_xml_file, cmp_xml_file], stdout=sp.PIPE, universal_newlines=True)
        self.assertEqual(proc_compare_xml.stdout, 'Comparison ended successfully\n')

    def run_test(self, jack_path_input):
        # Run my JackAnalyzer to generate xml file
        proc_run_JackAnalyzer = sp.run([self.my_jack_analyzer.as_posix(), jack_path_input.as_posix()], stdout=sp.PIPE, universal_newlines=True)
        # Use given compare tool to compare generated xml file
        if jack_path_input.is_file():
            jackfile = jack_path_input
            self.compare_output_file(jackfile)
        else:	# jack_path_input is dir
            jackfiles = [f for f in jack_path_input.glob('*.jack')]
            for jackfile in jackfiles:
                self.compare_output_file(jackfile)

    def test_ArrayTest(self):
        path_input = self.cwd / 'test/ArrayTest/Main.jack'
        self.run_test(path_input)

    def test_ExpressionLessSquare(self):
        path_input = self.cwd / 'test/ExpressionLessSquare'
        self.run_test(path_input)

    def test_Square(self):
        path_input = self.cwd / 'test/Square'
        self.run_test(path_input)

if __name__ == '__main__':
    unittest.main()
