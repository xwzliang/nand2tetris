#!/usr/bin/python3

import unittest
import shutil
from pathlib import Path
import subprocess as sp

class OperatingSystem(unittest.TestCase):

    def setUp(self):
        self.cwd = Path.cwd()
        self.given_compile_tool = self.cwd.parent / 'tools/JackCompiler.sh'

    def copy_and_compile(self, jack_class):
        test_dir = self.cwd / 'test' / (jack_class.stem + 'Test')
        # Copy jack class file to test_dir
        shutil.copy2(jack_class, test_dir)
        # Run JackCompiler to generate vm file
        proc_compile = sp.run([self.given_compile_tool.as_posix(), test_dir.as_posix()], stdout=sp.PIPE, universal_newlines=True)
        jack_class_vm_file = test_dir / jack_class.with_suffix('.vm').name
        self.assertTrue(jack_class_vm_file.exists())
        # After compilation succeeds, still need to test using given VMEmulator.sh tool

    def test_class_Math(self):
        jack_class = self.cwd / 'Math.jack'
        self.copy_and_compile(jack_class)

if __name__ == '__main__':
    unittest.main()
