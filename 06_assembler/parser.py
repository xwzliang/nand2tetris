from code_to_bin import Code2Bin
from symbol_table import SymbolTable

class Parser():
    """Parser: Encapsulates access to the input code. Reads an assembly language command, parses it, and provides convenient access to the command's components (fields and symbols). In addition, removes all white space and comments."""

    def __init__(self, in_file):
        """Get the input file and gets ready to parse it. Instantiate a Code2bin for binary translation"""
        self.in_file = in_file
        self.code2bin = Code2Bin()
        self.symb_table = SymbolTable()

    def read_in_file(self):
        """Read the input file and process lines, put lines containing codes to a buffer"""
        self.code_contents = []
        ROM_address = 0
        with open(self.in_file, 'r', encoding='utf_8') as inf:
            for line in inf:
                command = self.process(line)
                # If returned command is an empty line after processed, skip it
                if not command:
                    continue
                self.code_contents.append(command)
                cmd_type = self.command_type(command)
                if cmd_type == 'L_COMMAND':	# cmd_type is 'L_COMMAND', add new entry to the symbol table
                    symbol = self.get_symbol(command)
                    self.symb_table.add_entry(symbol, ROM_address)
                else:
                    ROM_address += 1

    def process(self, line):
        """Removes all white space and comments"""
        return line.split('//')[0].strip()

    def command_type(self, command):
        """
        Returns the type of the current command: 
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump (Either the dest or jump fields may be empty. If dest is empty, the "=" is omitted; If jump is empty, the ";" is omitted.)
        L_COMMAND (pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if '@' in command:
            return 'A_COMMAND'
        elif '=' in command or ';' in command:
            return 'C_COMMAND'
        elif '(' in command and ')' in command:
            return 'L_COMMAND'

    def get_symbol(self, command):
        """Returns the symbol or decimal Xxx of the current command @Xxx or (Xxx). Should be called only when command_type() is A_COMMAND or L_COMMAND.""" 
        return command.replace('@', '').replace('(', '').replace(')', '')

    def get_dest_comp_jump(self, command):
        """Returns the dest, comp, jump mnemonic in the current C-command. Should be called only when command_type()is C_COMMAND"""
        if ';' not in command:
            dest = command.split('=')[0]
            comp = command.split('=')[1]
            jump = 'null'
        elif '=' not in command:
            dest = 'null'
            comp = command.split(';')[0]
            jump = command.split(';')[1]
        else:
            dest = command.split('=')[0]
            comp = command.split('=')[1].split(';')[0]
            jump = command.split('=')[1].split(';')[1]
        return dest, comp, jump

    def translate(self):
        """Second pass, translate code_contents to binary contens"""
        self.out_binarys = []
        available_RAM_address = 16
        for command in self.code_contents:
            cmd_type = self.command_type(command)
            if cmd_type == 'A_COMMAND':
                symbol = self.get_symbol(command)
                if symbol.isdigit():
                    binary_line =  '0{:015b}'.format(int(symbol))
                    self.out_binarys.append(binary_line)
                elif self.symb_table.contains(symbol):
                    binary_line =  '0{:015b}'.format(int(self.symb_table.get_address(symbol)))
                    self.out_binarys.append(binary_line)
                else:
                    self.symb_table.add_entry(symbol, available_RAM_address)
                    binary_line =  '0{:015b}'.format(available_RAM_address)
                    self.out_binarys.append(binary_line)
                    available_RAM_address += 1
            elif cmd_type == 'C_COMMAND':
                dest, comp, jump = self.get_dest_comp_jump(command)
                dest_binary = self.code2bin.dest2bin(dest)
                comp_binary = self.code2bin.comp2bin(comp)
                jump_binary = self.code2bin.jump2bin(jump)
                binary_line =  '111' + comp_binary + dest_binary + jump_binary
                self.out_binarys.append(binary_line)

    def write_out_binarys(self):
        out_file = self.in_file.replace('asm', 'hack')
        with open(out_file, 'w', encoding='utf_8') as outf:
            for binary in self.out_binarys:
                outf.write(binary + '\n')
        print(out_file, 'finished assembling.')

    def parse(self):
        self.read_in_file()
        self.translate()
        self.write_out_binarys()

