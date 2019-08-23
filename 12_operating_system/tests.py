#!/usr/bin/python3

import unittest
import shutil
from pathlib import Path
import subprocess as sp

class OperatingSystem(unittest.TestCase):

    def setUp(self):
        self.cwd = Path.cwd()
        self.given_compile_tool = self.cwd.parent / 'tools/JackCompiler.sh'
        self.given_vm_emulator_tool = self.cwd.parent / 'tools/VMEmulator.sh'

    def copy_compile_and_compare(self, jack_class, should_compare):
        # If use VMEmulator in command line (i.e. should_compare is True), you need copy all the OS vm files from tools folder first, then compile them using this script, but if in interactive mode, you wouldn't have to, this is just the limitation of the given program
        test_dir = self.cwd / 'test' / (jack_class.stem + 'Test')
        # Copy jack class file to test_dir
        shutil.copy2(jack_class, test_dir)
        # Run JackCompiler to generate vm file
        proc_compile = sp.run([self.given_compile_tool.as_posix(), test_dir.as_posix()], stdout=sp.PIPE, universal_newlines=True)
        jack_class_vm_file = test_dir / jack_class.with_suffix('.vm').name
        self.assertTrue(jack_class_vm_file.exists())
        # After compilation succeeds, still need to test using given VMEmulator.sh tool
        if should_compare:
            test_file = test_dir / (test_dir.name + '.tst')
            proc_compare = sp.run([self.given_vm_emulator_tool.as_posix(), test_file.as_posix()], stdout=sp.PIPE, universal_newlines=True)
            self.assertEqual(proc_compare.stdout, 'End of script - Comparison ended successfully\n')

    def test_class_Math(self):
        jack_class = self.cwd / 'Math.jack'
        self.copy_compile_and_compare(jack_class, True)

    def test_class_Memory(self):
        jack_class = self.cwd / 'Memory.jack'
        self.copy_compile_and_compare(jack_class, True)

    def test_class_Array(self):
        jack_class = self.cwd / 'Array.jack'
        self.copy_compile_and_compare(jack_class, True)

    def test_class_String(self):
        jack_class = self.cwd / 'String.jack'
        self.copy_compile_and_compare(jack_class, False)

    def test_class_Screen(self):
        jack_class = self.cwd / 'Screen.jack'
        self.copy_compile_and_compare(jack_class, False)

    def test_class_Output(self):
        jack_class = self.cwd / 'Output.jack'
        self.copy_compile_and_compare(jack_class, False)

    def test_class_Keyboard(self):
        jack_class = self.cwd / 'Keyboard.jack'
        self.copy_compile_and_compare(jack_class, False)

    def test_class_Sys(self):
        jack_class = self.cwd / 'Sys.jack'
        self.copy_compile_and_compare(jack_class, False)

if __name__ == '__main__':
    unittest.main()
