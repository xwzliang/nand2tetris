class CodeWriter:
    """CodeWriter: Translates VM commands into Hack assembly code."""
    def __init__(self, command_contents, out_file):
        self.out_file = out_file
        self.command_contents = command_contents

    def translate_arithmetic(self, operator, index):
        """Generate the assembly code that is the translation of the given arithmetic command."""
        assembly_codes = []
        if operator == 'add':
            assembly_codes = [
                    	      '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'M=D+M',	# X=Y+X
                              ]
        elif operator == 'sub':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'M=M-D',	# X=X-Y
                              ]
        elif operator == 'neg':
            assembly_codes = [
                              '@SP', 
                              'A=M-1',
                              'M=-M',	# Y=-Y
                              ]
        elif operator == 'eq':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'D=M-D',	# D=X-Y
                              '@IS_EQUAL_{}'.format(index), 
                              'D;JEQ',	# if D=0 jump to label IS_EQUAL
                              '@SP',
                              'A=M-1',
                              'M=0',	# if D!=0, M=False
                              '@END_COMPARE_EQ_{}'.format(index),
                              '0;JMP',	# jump to label END_COMPARE
                              '(IS_EQUAL_{})'.format(index),	# define label IS_EQUAL
                              '@SP',
                              'A=M-1',
                              'M=-1',	# D=0 so M=True(-1)
                              '(END_COMPARE_EQ_{})'.format(index)	# define label END_COMPARE
                              ]
        elif operator == 'gt':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'D=M-D',	# D=X-Y
                              '@IS_GREATER_{}'.format(index), 
                              'D;JGT',	# if D>0 jump to label IS_GREATER
                              '@SP',
                              'A=M-1',
                              'M=0',	# D<=0, M=False
                              '@END_COMPARE_GT_{}'.format(index),
                              '0;JMP',	# jump to label END_COMPARE
                              '(IS_GREATER_{})'.format(index),	# define label IS_GREATER
                              '@SP',
                              'A=M-1',
                              'M=-1',	# D>0 so M=True(-1)
                              '(END_COMPARE_GT_{})'.format(index)	# define label END_COMPARE
                              ]
        elif operator == 'lt':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'D=M-D',	# D=X-Y
                              '@IS_LESS_{}'.format(index), 
                              'D;JLT',	# if D<0 jump to label IS_LESS
                              '@SP',
                              'A=M-1',
                              'M=0',	# D>=0, M=False
                              '@END_COMPARE_LT_{}'.format(index),
                              '0;JMP',	# jump to label END_COMPARE
                              '(IS_LESS_{})'.format(index),	# define label IS_LESS
                              '@SP',
                              'A=M-1',
                              'M=-1',	# D<0 so M=True(-1)
                              '(END_COMPARE_LT_{})'.format(index)	# define label END_COMPARE
                              ]
        elif operator == 'and':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'M=D&M',	# M=Y&X
                              ]
        elif operator == 'or':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'M=D|M',	# M=Y|X
                              ]
        elif operator == 'not':
            assembly_codes = [
                              '@SP', 
                              'A=M-1',
                              'M=!M',	# Y=!Y
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
        for command_index, command_content in enumerate(self.command_contents):
            cmd_type = command_content[0]
            command = command_content[-1]
            assembly_codes = []
            if cmd_type == 'C_ARITHMETIC':
                operator = command_content[1]
                # Pass command_index to translate_arithmetic method for generating unique labels at runtime
                assembly_codes = self.translate_arithmetic(operator, command_index)
            elif cmd_type == 'C_PUSH' or cmd_type == 'C_POP':
                memory_segment, index = command_content[1]
                assembly_codes = self.translate_push_pop(cmd_type, memory_segment, index)
            output_codes.append('// {}'.format(command))	# Write command itself as comment for inspection
            output_codes += assembly_codes
        with open(self.out_file, 'w', encoding='utf_8') as outf:
            for code_line in output_codes:
                outf.write(str(code_line) + '\n')
