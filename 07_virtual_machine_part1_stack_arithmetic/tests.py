#!/usr/bin/python3

import unittest
from pathlib import Path
import subprocess as sp

class VMtranslator(unittest.TestCase):

    def setUp(self):
        self.cwd = Path.cwd()
        self.given_cpu_emulator_tool = self.cwd.parent / 'tools/CPUEmulator.sh'
        self.my_vm_translator = self.cwd / 'VMtranslator.py'

    def run_test(self, vm_file):
        asm_file = vm_file.with_suffix('.asm')
        tst_file = vm_file.with_suffix('.tst')
        # Run my VMtranslator to generate asm file
        proc_translate = sp.run([self.my_vm_translator.as_posix(), vm_file.as_posix()], stdout=sp.PIPE, universal_newlines=True)
        self.assertEqual(proc_translate.stdout, 'Successfully translate to assembly ' + asm_file.as_posix() + '\n')
        self.assertTrue(asm_file.exists())
        # Use given CPU emulator to compare generated asm file
        proc_compare = sp.run([self.given_cpu_emulator_tool.as_posix(), tst_file], stdout=sp.PIPE, universal_newlines=True)
        self.assertEqual(proc_compare.stdout, 'End of script - Comparison ended successfully\n')

    def test_stack_arithmetic_simple_add(self):
        vm_file = self.cwd / 'test/StackArithmetic/SimpleAdd/SimpleAdd.vm'
        self.run_test(vm_file)

    def test_stack_arithmetic_stack_test(self):
        vm_file = self.cwd / 'test/StackArithmetic/StackTest/StackTest.vm'
        self.run_test(vm_file)

    def test_memory_access_basic_test(self):
        vm_file = self.cwd / 'test/MemoryAccess/BasicTest/BasicTest.vm'
        self.run_test(vm_file)

    def test_memory_access_pointer_test(self):
        vm_file = self.cwd / 'test/MemoryAccess/PointerTest/PointerTest.vm'
        self.run_test(vm_file)

    def test_memory_access_static_test(self):
        vm_file = self.cwd / 'test/MemoryAccess/StaticTest/StaticTest.vm'
        self.run_test(vm_file)

if __name__ == '__main__':
    unittest.main()
