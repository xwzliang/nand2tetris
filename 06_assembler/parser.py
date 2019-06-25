
class Parser():
    """Parser: Encapsulates access to the input code. Reads an assembly language command, parses it, and provides convenient access to the command's components (fields and symbols). In addition, removes all white space and comments."""

    def __init__(self, in_file):
        """Get the input file and gets ready to parse it."""
        self.in_file = in_file

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

    def parse(self):
        with open(self.in_file, 'r', encoding='utf_8') as inf:
            for line in inf:
                command = self.process(line)
                # If returned command is an empty line after processed, skip it
                if not command:
                    continue
                cmd_type = self.command_type(command)
                if cmd_type == 'A_COMMAND' or cmd_type == 'L_COMMAND':
                    symbol = self.get_symbol(command)
                    print(symbol)
                else:
                    dest, comp, jump = self.get_dest_comp_jump(command)
                    print(dest, comp, jump)

