class CodeWriter:
    """CodeWriter: Translates VM commands into Hack assembly code."""
    def __init__(self, command_contents, out_file):
        self.out_file = out_file
        self.command_contents = command_contents

    def translate_arithmetic(self, operator):
        """Generate the assembly code that is the translation of the given arithmetic command."""
        assembly_codes = []
        if operator == 'add':
            assembly_codes = [
                    	      '@SP', 
                    	      'M=M-1',	# SP--
                              'A=M',
                              'D=M',	# D=Y
                              'A=A-1',
                              'M=D+M',	# X=Y+X
                              ]
        return assembly_codes

    def translate_push_pop(self, cmd_type, memory_segment, index):
        """Generate the assembly code that is the translation of the given push or pop memory access command."""
        assembly_codes = []
        if cmd_type == 'C_PUSH':
            if memory_segment == 'constant':
                assembly_codes = [
                        	  '@{}'.format(index),	# A=constant i
                                  'D=A',	# D=constant i
                                  '@SP',
                                  'A=M',
                                  'M=D',	# *SP=constant i
                                  '@SP',
                                  'M=M+1',	# SP++
                        ]
        return assembly_codes

    def write(self):
        """Translate and write translated assembly code to out_file"""
        output_codes = []
        for command_content in self.command_contents:
            cmd_type = command_content[0]
            command = command_content[-1]
            assembly_codes = []
            if cmd_type == 'C_ARITHMETIC':
                operator = command_content[1]
                assembly_codes = self.translate_arithmetic(operator)
            elif cmd_type == 'C_PUSH' or cmd_type == 'C_POP':
                memory_segment, index = command_content[1]
                assembly_codes = self.translate_push_pop(cmd_type, memory_segment, index)
            output_codes.append('// {}'.format(command))	# Write command itself as comment for inspection
            output_codes += assembly_codes
        with open(self.out_file, 'w', encoding='utf_8') as outf:
            for code_line in output_codes:
                outf.write(str(code_line) + '\n')
