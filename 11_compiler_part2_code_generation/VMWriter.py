class VMWriter:
    """VMWriter: Emits VM commands into a file, using the VM command syntax."""
    def __init__(self, out_vm_file):
        """Creates a new file and prepares it for writing."""
        self.outf = open(out_vm_file, 'w', encoding='utf_8')

    def write_push(self, segment, index):
        """
        Writes a VM push command.
        Arguments:
        	segment (const, arg, local, static, this, that, pointer, temp) 
                index (int)
        """
        command = 'push {} {}'.format(segment, index)
        self.outf.write(command + '\n')

    def write_pop(self, segment, index):
        """
        Writes a VM pop command.
        Arguments:
        	segment (const, arg, local, static, this, that, pointer, temp) 
                index (int)
        """
        command = 'pop {} {}'.format(segment, index)
        self.outf.write(command + '\n')

    def write_arithmetic(self, arithmetic_cmd):
        """
        Writes a VM arithmetic command.
        Arguments:
        	arithmetic_cmd (add, sub, neg, eq, gt, lt, and, or, not)
        """
        command = arithmetic_cmd
        self.outf.write(command + '\n')

    def write_label(self, label):
        """Writes a VM label command"""
        command = 'label {}'.format(label)
        self.outf.write(command + '\n')

    def write_goto(self, label):
        """Writes a VM label command"""
        command = 'goto {}'.format(label)
        self.outf.write(command + '\n')

    def write_if(self, label):
        """Writes a VM if-goto command"""
        command = 'if-goto {}'.format(label)
        self.outf.write(command + '\n')

    def write_call(self, function_name, args_num):
        """Writes a VM call command"""
        command = 'call {} {}'.format(function_name, args_num)
        self.outf.write(command + '\n')

    def write_function(self, function_name, local_vars_num):
        """Writes a VM function command"""
        command = 'function {} {}'.format(function_name, local_vars_num)
        self.outf.write(command + '\n')

    def write_return(self):
        """Writes a VM return command"""
        command = 'return'
        self.outf.write(command + '\n')

    def close(self):
        """Close the output file"""
        self.outf.close()
