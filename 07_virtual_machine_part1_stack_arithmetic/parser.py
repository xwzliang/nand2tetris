class Parser:
    """
    Parser: Handles the parsing of a single .vm file, and encapsulates access to the input code. It reads VM commands, parses them, and provides convenient access to their components. In addition, it removes all white space and comments.
    """
    def __init__(self, in_file):
        self.in_file = in_file

    def process(self, line):
        """Removes all white space and comments"""
        return line.split('//')[0].strip()

    def get_command_type(self, command):
        """Returns the type of the current VM command. C_ARITHMETIC is returned for all the arithmetic commands."""
        first_word_in_command = command.split(' ')[0]
        if any(command==c for c in ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not')):
            return 'C_ARITHMETIC'
        elif first_word_in_command == 'push':
            return 'C_PUSH'
        elif first_word_in_command == 'pop':
            return 'C_POP'
        elif first_word_in_command == 'label':
            return 'C_LABEL'
        elif first_word_in_command == 'goto':
            return 'C_GOTO'
        elif first_word_in_command == 'if-goto':
            return 'C_IF'
        elif first_word_in_command == 'function':
            return 'C_FUNCTION'
        elif first_word_in_command == 'call':
            return 'C_CALL'
        elif command == 'return':
            return 'C_RETURN'

    def get_arguments(self, command, cmd_type):
        """Returns arguments of given command and cmd_type"""
        if cmd_type == 'C_ARITHMETIC':
            arguments = command
        elif cmd_type == 'C_RETURN':
            arguments = None
        else:
            arguments = command.split(' ')[1:]
        return arguments

    def parse(self):
        """Read input file, parses commands, returns contents with command type and arguments (if any)"""
        returned_contents = []
        with open(self.in_file, 'r', encoding='utf_8') as inf:
            for line in inf:
                command = self.process(line)
                # If returned command is an empty line after processed, skip it
                if not command:
                    continue
                cmd_type = self.get_command_type(command)
                arguments = self.get_arguments(command, cmd_type)
                returned_content = [cmd_type, arguments] if arguments else [cmd_type]
                returned_contents.append(returned_content)
        return returned_contents
