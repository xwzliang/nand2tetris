import re

class JackTokenizer:
    """JackTokenizer: Removes all comments and white space from the input stream and breaks it into Jack-language tokens, as specified by the Jack grammar"""
    def __init__(self, in_file):
        self.in_file = in_file
        self.construct_symbols()
        self.construct_keywords()

    def construct_symbols(self):
        """Put all symbols defined by Jack language into self.symbols"""
        self.symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}

    def construct_keywords(self):
        """Put all keywords defined by Jack language into self.keywords"""
        self.keywords = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'}

    def tokenize(self):
        tokens = self.process_input()
        tokens_with_tokenType = self.generate_type_for_tokens(tokens)
        output_for_write = self.generate_output_for_tokens(tokens_with_tokenType)
        return tokens_with_tokenType

    def process_input(self):
        self.skip = False
        tokens = []
        with open(self.in_file, 'r', encoding='utf_8') as inf:
            for line in inf:
                if self.should_skip(line):
                    continue
                code_content_in_line = self.rm_comments_white_space(line)
                # Process code_content_in_line
                tokens_from_line = self.get_tokens_from_code(code_content_in_line)
                tokens += tokens_from_line
        return tokens

    def should_skip(self, line):
        """Determine whether line parameter should be skiped according different comment type"""
        # Handle comments in the format /* */
        if '/*' in line or self.skip:
            if '*/' in line:
                self.skip = False
            else:
                # if */ not encountered, set skip to True to skip more lines
                self.skip = True
            return True
        # Handle comments in the format // and return code content
        else:
            code_content_in_line = self.rm_comments_white_space(line)
            if not code_content_in_line:
                # If returned content is none, skip this line
                return True
            return False

    def rm_comments_white_space(self, line):
        """Removes all white space and comments start with //"""
        return line.split('//')[0].strip()
        
    def get_tokens_from_code(self, code_content_in_line):
        return_tokens = []
        is_new_token = True
        is_in_string = False
        for char in code_content_in_line:
            if char is '"':
                if is_in_string:
                    return_tokens[-1] += char
                else:
                    return_tokens.append(char)
                is_in_string = not is_in_string
                is_new_token = not is_in_string
            elif char is ' ' and not is_in_string:
                is_new_token = True
            elif char in self.symbols and not is_in_string:
                return_tokens.append(char)
                is_new_token = True
            else:
                if is_new_token:
                    # If is new token, create a new item in return_tokens list
                    return_tokens.append(char)
                    is_new_token = False
                else:
                    return_tokens[-1] += char
        return return_tokens

    def generate_type_for_tokens(self, tokens):
        tokens_with_tokenType = []
        for token in tokens:
            token_type = self.get_type_for_token(token)
            tokens_with_tokenType.append((token, token_type))
        return tokens_with_tokenType

    def get_type_for_token(self, token):
        if token in self.symbols:
            return 'symbol'
        elif token in self.keywords:
            return 'keyword'
        elif token.isdigit():
            return 'integerConstant'
        elif token[0] == '"' and token[-1] == '"' and len(token)>1:	# A single " is invalid
            return 'stringConstant'
        elif re.match('[a-zA-Z_][a-zA-Z0-9_]*', token):		# Valid identifier is a sequence of letters, digits, and underscore ('_') not starting with a digit
            return 'identifier'

    def generate_output_for_tokens(self, tokens_with_tokenType):
        output_for_write = []
        for token, token_type in tokens_with_tokenType:
            if token_type == 'symbol':
                if token == '<':
                    token_for_write = '&lt;'
                elif token == '>':
                    token_for_write = '&gt;'
                elif token == '&':
                    token_for_write = '&amp;'
                else:
                    token_for_write = token
            elif token_type == 'stringConstant':
                # remove the double quote at the beginning and end
                token_for_write = token[1:-1]
            else:
                token_for_write = token
            output_line = '<{0}> {1} </{0}>'.format(token_type, token_for_write)
            output_for_write.append(output_line)
        return output_for_write

