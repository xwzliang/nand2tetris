#!/usr/bin/python3

import unittest
from pathlib import Path
import subprocess as sp

class VMtranslator(unittest.TestCase):

    def setUp(self):
        self.cwd = Path.cwd()
        self.given_vm_emulator_tool = self.cwd.parent / 'tools/VMEmulator.sh'
        self.my_vm_translator = self.cwd / 'VMtranslator.py'

    def test_stack_arithmetic_simple_add(self):
        simple_add_vm = self.cwd / 'test/StackArithmetic/SimpleAdd/SimpleAdd.vm'
        simple_add_asm = simple_add_vm.with_suffix('.asm')
        simple_add_tst = simple_add_vm.parent / 'SimpleAddVME.tst'
        # Run my VMtranslator to generate asm file
        proc_translate = sp.run([self.my_vm_translator.as_posix(), simple_add_vm.as_posix()], stdout=sp.PIPE, universal_newlines=True)
        self.assertEqual(proc_translate.stdout, 'Successfully translate to assembly ' + simple_add_asm.as_posix() + '\n')
        self.assertTrue(simple_add_asm.exists())
        # Use given vm emulator to compare generated asm file
        proc_compare = sp.run([self.given_vm_emulator_tool.as_posix(), simple_add_tst], stdout=sp.PIPE, universal_newlines=True)
        self.assertEqual(proc_compare.stdout, 'End of script - Comparison ended successfully\n')

if __name__ == '__main__':
    unittest.main()
