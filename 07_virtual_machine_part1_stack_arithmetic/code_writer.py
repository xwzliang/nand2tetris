class CodeWriter:
    """CodeWriter: Translates VM commands into Hack assembly code."""
    def __init__(self, code_contents, out_file):
        self.out_file = out_file
        self.code_contents = code_contents
        self.dynamic_memory_base_dict = {'argument': 'ARG',
                                         'local': 'LCL',
                                         'this': 'THIS',
                                         'that': 'THAT'}
        self.fixed_memory_base_dict = {'pointer': '3',
                		       'temp': '5'}

    def translate_arithmetic(self, operator, command_index):
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
                              '@IS_EQUAL_{}'.format(command_index), 
                              'D;JEQ',	# if D=0 jump to label IS_EQUAL
                              '@SP',
                              'A=M-1',
                              'M=0',	# if D!=0, M=False
                              '@END_COMPARE_EQ_{}'.format(command_index),
                              '0;JMP',	# jump to label END_COMPARE
                              '(IS_EQUAL_{})'.format(command_index),	# define label IS_EQUAL
                              '@SP',
                              'A=M-1',
                              'M=-1',	# D=0 so M=True(-1)
                              '(END_COMPARE_EQ_{})'.format(command_index)	# define label END_COMPARE
                              ]
        elif operator == 'gt':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'D=M-D',	# D=X-Y
                              '@IS_GREATER_{}'.format(command_index), 
                              'D;JGT',	# if D>0 jump to label IS_GREATER
                              '@SP',
                              'A=M-1',
                              'M=0',	# D<=0, M=False
                              '@END_COMPARE_GT_{}'.format(command_index),
                              '0;JMP',	# jump to label END_COMPARE
                              '(IS_GREATER_{})'.format(command_index),	# define label IS_GREATER
                              '@SP',
                              'A=M-1',
                              'M=-1',	# D>0 so M=True(-1)
                              '(END_COMPARE_GT_{})'.format(command_index)	# define label END_COMPARE
                              ]
        elif operator == 'lt':
            assembly_codes = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                              'D=M-D',	# D=X-Y
                              '@IS_LESS_{}'.format(command_index), 
                              'D;JLT',	# if D<0 jump to label IS_LESS
                              '@SP',
                              'A=M-1',
                              'M=0',	# D>=0, M=False
                              '@END_COMPARE_LT_{}'.format(command_index),
                              '0;JMP',	# jump to label END_COMPARE
                              '(IS_LESS_{})'.format(command_index),	# define label IS_LESS
                              '@SP',
                              'A=M-1',
                              'M=-1',	# D<0 so M=True(-1)
                              '(END_COMPARE_LT_{})'.format(command_index)	# define label END_COMPARE
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

    def translate_push_pop(self, filename, cmd_type, memory_segment, memory_index):
        """Generate the assembly code that is the translation of the given push or pop memory access command."""
        assembly_codes = []
        if cmd_type == 'C_PUSH':
            if memory_segment == 'constant':
                assembly_codes = [
                        	  '@{}'.format(memory_index),	# A=constant i
                                  'D=A',	# D=constant i
                                  '@SP',
                                  'A=M',
                                  'M=D',	# *SP=constant i
                                  '@SP',
                                  'M=M+1',	# SP++
                        ]
            elif memory_segment == 'static':
                assembly_codes = [
                                  '@{}.{}'.format(filename, memory_index),	# Trick: static j should be translated to @filename.j
                                  'D=M',	# Get the content to D
                                  '@SP',
                                  'A=M',
                                  'M=D',	# *SP=D
                                  '@SP',
                                  'M=M+1',	# SP++
                                 ]
            elif memory_segment == 'pointer' or memory_segment == 'temp':
                assembly_codes = [
                        	  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.fixed_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'A=D+A',	# Get the address: memory index + momory base (stored as fixed number, so use A)
                                  'D=M',	# Get the content to D
                                  '@SP',
                                  'A=M',
                                  'M=D',	# *SP=D
                                  '@SP',
                                  'M=M+1',	# SP++
                                 ]
            else:	# memory_segment in ['argument', 'local', 'this', 'that']
                assembly_codes = [
                        	  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.dynamic_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'A=D+M',	# Get the address: memory index + momory base (stored in register pointers, so use M)
                                  'D=M',	# Get the content to D
                                  '@SP',
                                  'A=M',
                                  'M=D',	# *SP=D
                                  '@SP',
                                  'M=M+1',	# SP++
                                 ]
        else:	# cmd_type == 'C_POP'
            if memory_segment == 'static':
                assembly_codes = [
                                  '@{}.{}'.format(filename, memory_index),	# Trick: static j should be translated to @filename.j
                                  'D=A',	# Put the address to D
                                  '@SP',
                                  'A=M',	# Get to the place which SP points to
                                  'M=D',	# Dump address stored in D to M
                                  'A=A-1',
                                  'D=M',	# D=*SP
                                  'A=A+1',	# Get to the place where address is stored
                                  'A=M',	# Get to the place where address points to
                                  'M=D',	# Write value stored in D to M
                                  '@SP',
                                  'M=M-1',	# SP--
                                 ]
            elif memory_segment == 'pointer' or memory_segment == 'temp':
                assembly_codes = [
                                  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.fixed_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'D=D+A',	# Get the address: memory index + momory base, and stored in D
                                  '@SP',
                                  'A=M',	# Get to the address which SP points to
                                  'M=D',	# Dump address stored in D to M
                                  'A=A-1',
                                  'D=M',	# D=*SP
                                  'A=A+1',	# Get to the place where address is stored
                                  'A=M',	# Get to the place where address points to
                                  'M=D',	# Write value stored in D to M
                                  '@SP',
                                  'M=M-1',	# SP--
                                 ]
            else:	# memory_segment in ['argument', 'local', 'this', 'that']
                assembly_codes = [
                                  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.dynamic_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'D=D+M',	# Get the address: memory index + momory base, and stored in D
                                  '@SP',
                                  'A=M',	# Get to the address which SP points to
                                  'M=D',	# Dump address stored in D to M
                                  'A=A-1',
                                  'D=M',	# D=*SP
                                  'A=A+1',	# Get to the place where address is stored
                                  'A=M',	# Get to the place where address points to
                                  'M=D',	# Write value stored in D to M
                                  '@SP',
                                  'M=M-1',	# SP--
                                 ]
        return assembly_codes

    def write(self):
        """Translate and write translated assembly code to out_file"""
        output_codes = []
        for filename, command_contents in self.code_contents.items():
            for command_index, command_content in enumerate(command_contents):
                cmd_type = command_content[0]
                command = command_content[-1]
                assembly_codes = []
                if cmd_type == 'C_ARITHMETIC':
                    operator = command_content[1]
                    # Pass command_index to translate_arithmetic method for generating unique labels at runtime
                    assembly_codes = self.translate_arithmetic(operator, command_index)
                elif cmd_type == 'C_PUSH' or cmd_type == 'C_POP':
                    memory_segment, memory_index = command_content[1]
                    assembly_codes = self.translate_push_pop(filename, cmd_type, memory_segment, memory_index)
                output_codes.append('// {}'.format(command))	# Write command itself as comment for inspection
                output_codes += assembly_codes
        with open(self.out_file, 'w', encoding='utf_8') as outf:
            for code_line in output_codes:
                outf.write(str(code_line) + '\n')
