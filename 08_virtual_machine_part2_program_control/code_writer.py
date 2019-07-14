class CodeWriter:
    """CodeWriter: Translates VM commands into Hack assembly code."""
    def __init__(self, code_contents, out_file):
        self.out_file = out_file
        self.code_contents = code_contents
        self.setup_for_asm_code_translation()
        self.function_call_times = 0	# Use this to count the function calls, which helps to generate unique function return label

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
        self.asm_code_memory_push_0 = [
                              '@SP',
                              'A=M',
                              'M=0',	# *SP=0
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

    def asm_code_memory_push_content_in_pointer(self, pointer_name):
        """Push the content of the pointer (LCL, ARG, THIS or THAT) to the stack"""
        assembly_codes = [
                '@{}'.format(pointer_name),
                'D=M',
                *self.asm_code_memory_push_content_in_D
                ]
        return assembly_codes

    def asm_code_memory_restore_pointer_value(self, pointer_name, num_above_LCL):
        """Restore the value of pointer, given the pointer name and the location number above LCL"""
        assembly_codes = [
                '@{}'.format(num_above_LCL),
                'D=A',
                '@LCL',
                'A=M-D',
                'D=M',
                '@{}'.format(pointer_name),
                'M=D',	# Restore the value of pointer (pointer_name) of the caller: pointer_name=*(LCL-num_above_LCL)
                ]
        return assembly_codes

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

    def translate_function(self, function_name, local_variable_num):
        """Writes assembly code that effects the function command."""
        assembly_codes = [
                '({})'.format(function_name),	# Generate a label of function_name
                ] + int(local_variable_num) * self.asm_code_memory_push_0	# Initialize all local_variable_num of varibles to 0 by push 0 to stack
        return assembly_codes

    def translate_call_function(self, function_name, function_arg_num):
        """Writes assembly code that effects the call command."""
        self.function_call_times += 1	# Every time this function is called, function_call_times += 1
        return_address_label = 'return_address_{}_{}'.format(function_name, self.function_call_times)	# Use function_call_times to generate uniqu return label
        assembly_codes = [
                '@{}'.format(return_address_label),
                'D=A',
                *self.asm_code_memory_push_content_in_D,		# push return address to stack
                *self.asm_code_memory_push_content_in_pointer('LCL'),		# push content of LCL to stack
                *self.asm_code_memory_push_content_in_pointer('ARG'),		# push content of ARG to stack
                *self.asm_code_memory_push_content_in_pointer('THIS'),		# push content of THIS to stack
                *self.asm_code_memory_push_content_in_pointer('THAT'),		# push content of THAT to stack
                '@5',
                'D=A',	# D=5
                '@{}'.format(function_arg_num),
                'D=D+A',	# D=function_arg_num + 5
                '@SP',
                'D=M-D',	# D=SP - function_arg_num - 5
                '@ARG',
                'M=D',	# Reposition ARG, ARG=SP - function_arg_num - 5
                '@SP',
                'D=M',
                '@LCL',
                'M=D',	# Reposition LCL, LCL=SP
                '@{}'.format(function_name),
                '0;JMP',	# Jump to function_name label
                '({})'.format(return_address_label),	# Define return_address_label
                ]
        return assembly_codes

    def translate_return(self):
        """Writes assembly code that effects the return command."""
        return_temp_var = 'return_temp_var_{}'.format(self.function_call_times)
        assembly_codes = [
                *self.asm_code_memory_restore_pointer_value(return_temp_var, 5),	# Put the return address of the caller to the temp location (R5) in RAM: R5=*(LCL-5)
                '@SP',
                'A=M-1',
                'D=M',	# Put content of *(SP-1) to D
                '@ARG',
                'A=M',
                'M=D',	# Put the returned value to *ARG: *ARG=*(SP-1): Put content of D to *ARG
                '@ARG',
                'D=M+1',
                '@SP',
                'M=D',	# Restore SP of the caller: SP=ARG+1
                '@LCL',
                'A=M-1',
                'D=M',
                '@THAT',
                'M=D',	# Restore THAT of the caller: THAT=*(LCL-1)
                *self.asm_code_memory_restore_pointer_value('THIS', 2),	# Restore THIS of the caller: THIS=*(LCL-2)
                *self.asm_code_memory_restore_pointer_value('ARG', 3),	# Restore ARG of the caller: ARG=*(LCL-3)
                *self.asm_code_memory_restore_pointer_value('LCL', 4),	# Restore LCL of the caller: LCL=*(LCL-4),
                '@{}'.format(return_temp_var),
                'A=M',
                '0;JMP',	# Go to the return address stored in R5
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

                elif cmd_type == 'C_FUNCTION':
                    function_name, local_variable_num = command_content[1]
                    assembly_codes = self.translate_function(function_name, local_variable_num)
                elif cmd_type == 'C_CALL':
                    function_name, function_arg_num = command_content[1]
                    assembly_codes = self.translate_call_function(function_name, function_arg_num)
                else:	# cmd_type == 'C_RETURN':
                    assembly_codes = self.translate_return()

                output_codes.append('// {}'.format(command))	# Write command itself as comment for inspection
                output_codes += assembly_codes
        return output_codes

    def write_bootstrap_code(self):
        """Writes assembly code that effects the VM initialization, also called bootstrap code. This code must be placed at the beginning of the output file."""
        assembly_codes = [
                '// SP=256',
                '@256',
                'D=A',
                '@SP',
                'M=D',	# SP=256
                '// call Sys.init 0',
                *self.translate_call_function('Sys.init', 0),
                ]
        return assembly_codes

    def write(self):
        """Translate and write translated assembly code to out_file"""
        sys_vm_file = self.out_file.parent / 'Sys.vm'
        if sys_vm_file.exists():
            # if Sys.vm exists, write bootstrap code at beginning of the output_codes
            output_codes = self.write_bootstrap_code() + self.translate()
        else:
            output_codes = self.translate()

        with open(self.out_file, 'w', encoding='utf_8') as outf:
            for code_line in output_codes:
                outf.write(str(code_line) + '\n')
