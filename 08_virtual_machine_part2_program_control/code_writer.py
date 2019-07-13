class CodeWriter:
    """CodeWriter: Translates VM commands into Hack assembly code."""
    def __init__(self, code_contents, out_file):
        self.out_file = out_file
        self.code_contents = code_contents
        self.setup_for_asm_code_translation()

    def setup_for_asm_code_translation(self):
        """Initialize common stuff which will be used in asm code translation"""
        self.dynamic_memory_base_dict = {'argument': 'ARG',
                                         'local': 'LCL',
                                         'this': 'THIS',
                                         'that': 'THAT'}
        self.fixed_memory_base_dict = {'pointer': '3',
                		       'temp': '5'}
        self.asm_code_operator_dict = {
                'add': 'M=D+M',	# M=Y+X'
                'sub': 'M=M-D',	# M=X-Y'
                'and': 'M=D&M',	# M=Y&X'
                'or': 'M=D|M',	# M=Y|X'
                'neg': 'M=-M',	# Y=-Y
                'not': 'M=!M',	# Y=!Y
                }              
        self.asm_code_arithmetic_make_DeqY_MeqX_SPminus1 = [
                              '@SP', 
                    	      'AM=M-1',	# SP--, A=M-1
                              'D=M',	# D=Y
                              'A=A-1',
                ]
        self.asm_code_memory_push_content_in_D = [
                              '@SP',
                              'A=M',
                              'M=D',	# *SP=constant i
                              '@SP',
                              'M=M+1',	# SP++
                ]
        self.asm_code_memory_pop_address_in_D = [
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

    def translate_arithmetic(self, filename, operator, command_index):
        """Generate the assembly code that is the translation of the given arithmetic command."""
        assembly_codes = []
        if operator in ['add', 'sub', 'and', 'or']:
            assembly_codes = [
                    *self.asm_code_arithmetic_make_DeqY_MeqX_SPminus1,
                    self.asm_code_operator_dict[operator],
                ]
        elif operator in ['neg', 'not']:
            assembly_codes = [
                    '@SP', 
                    'A=M-1',
                    self.asm_code_operator_dict[operator],
                ]
        else:	# operator is 'eq' or 'gt' or 'lt':
            op_upper = operator.upper()
            assembly_codes = [
                    *self.asm_code_arithmetic_make_DeqY_MeqX_SPminus1,
                    'D=M-D',	# D=X-Y
                    '@IS_{}_{}_{}'.format(op_upper, filename, command_index), 
                    'D;J{}'.format(op_upper),	# if D compares to 0 using specified operator succeeds, jump to label specified above
                    '@SP',
                    'A=M-1',
                    'M=0',	# if D compares to 0 using specified operator fails, M=False
                    '@END_COMPARE_{}_{}_{}'.format(op_upper, filename, command_index),
                    '0;JMP',	# jump to label END_COMPARE
                    '(IS_{}_{}_{})'.format(op_upper, filename, command_index),	# define label for successful coparision using specified operator
                    '@SP',
                    'A=M-1',
                    'M=-1',	# D compares to 0 succeeds, so M=True(-1)
                    '(END_COMPARE_{}_{}_{})'.format(op_upper, filename, command_index)	# define label END_COMPARE
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
                                  *self.asm_code_memory_push_content_in_D,
                        ]
            elif memory_segment == 'static':
                assembly_codes = [
                                  '@{}.{}'.format(filename, memory_index),	# Trick: static j should be translated to @filename.j
                                  'D=M',	# Get the content to D
                                  *self.asm_code_memory_push_content_in_D,
                                 ]
            elif memory_segment == 'pointer' or memory_segment == 'temp':
                assembly_codes = [
                        	  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.fixed_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'A=D+A',	# Get the address: memory index + momory base (stored as fixed number, so use A)
                                  'D=M',	# Get the content to D
                                  *self.asm_code_memory_push_content_in_D,
                                 ]
            else:	# memory_segment in ['argument', 'local', 'this', 'that']
                assembly_codes = [
                        	  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.dynamic_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'A=D+M',	# Get the address: memory index + momory base (stored in register pointers, so use M)
                                  'D=M',	# Get the content to D
                                  *self.asm_code_memory_push_content_in_D,
                                 ]
        else:	# cmd_type == 'C_POP'
            if memory_segment == 'static':
                assembly_codes = [
                                  '@{}.{}'.format(filename, memory_index),	# Trick: static j should be translated to @filename.j
                                  'D=A',	# Put the address to D
                                  *self.asm_code_memory_pop_address_in_D,
                                 ]
            elif memory_segment == 'pointer' or memory_segment == 'temp':
                assembly_codes = [
                                  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.fixed_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'D=D+A',	# Get the address: memory index + momory base, and stored in D
                                  *self.asm_code_memory_pop_address_in_D,
                                 ]
            else:	# memory_segment in ['argument', 'local', 'this', 'that']
                assembly_codes = [
                                  '@{}'.format(memory_index),	# A=memory_index
                                  'D=A',	# D=memory_index
                                  '@{}'.format(self.dynamic_memory_base_dict[memory_segment]),	# Get the memory base for memory_segment
                                  'D=D+M',	# Get the address: memory index + momory base, and stored in D
                                  *self.asm_code_memory_pop_address_in_D,
                                 ]
        return assembly_codes

    def translate_label(self, filename, label_name):
        """Writes assembly code that effects the label command."""
        assembly_codes = [
                '({}_{})'.format(label_name, filename),
                ]
        return assembly_codes

    def translate_goto(self, filename, label_name):
        """Writes assembly code that effects the goto command."""
        assembly_codes = [
                '@{}_{}'.format(label_name, filename),
                '0;JMP',
                ]
        return assembly_codes

    def translate_if_goto(self, filename, label_name):
        """Writes assembly code that effects the if-goto command."""
        assembly_codes = [
                '@SP',
                'AM=M-1',	# SP--, A=M-1
                'D=M',	# Store the value at top of stack to D register
                '@{}_{}'.format(label_name, filename),
                'D;JNE',	# If D != 0, then jump
                ]
        return assembly_codes

    def translate(self):
        """Translate vm code to assembly"""
        output_codes = []
        for filename, command_contents in self.code_contents.items():
            for command_index, command_content in enumerate(command_contents):
                cmd_type = command_content[0]
                command = command_content[-1]
                assembly_codes = []
                if cmd_type == 'C_ARITHMETIC':
                    operator = command_content[1]
                    # Pass filename and command_index to translate_arithmetic method for generating unique labels at runtime
                    assembly_codes = self.translate_arithmetic(filename, operator, command_index)
                elif cmd_type == 'C_PUSH' or cmd_type == 'C_POP':
                    memory_segment, memory_index = command_content[1]
                    assembly_codes = self.translate_push_pop(filename, cmd_type, memory_segment, memory_index)

                elif cmd_type == 'C_LABEL':
                    label_name, = command_content[1]
                    assembly_codes = self.translate_label(filename, label_name)	# Add filename to label name to ensure the label is unique
                elif cmd_type == 'C_GOTO':
                    label_name, = command_content[1]
                    assembly_codes = self.translate_goto(filename, label_name)	# Add filename to label name to ensure the label is unique
                elif cmd_type == 'C_IF':
                    label_name, = command_content[1]
                    assembly_codes = self.translate_if_goto(filename, label_name)	# Add filename to label name to ensure the label is unique

                output_codes.append('// {}'.format(command))	# Write command itself as comment for inspection
                output_codes += assembly_codes
        return output_codes

    def write(self):
        """Translate and write translated assembly code to out_file"""
        output_codes = self.translate()
        with open(self.out_file, 'w', encoding='utf_8') as outf:
            for code_line in output_codes:
                outf.write(str(code_line) + '\n')
