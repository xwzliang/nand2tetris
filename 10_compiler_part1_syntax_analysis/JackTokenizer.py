class JackTokenizer:
    """JackTokenizer: Removes all comments and white space from the input stream and breaks it into Jack-language tokens, as specified by the Jack grammar"""
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file

    def tokenize(self):
        self.process_input()
        self.write_output()

    def process_input(self):
        self.skip = False
        with open(self.in_file, 'r', encoding='utf_8') as inf:
            for line in inf:
                if self.should_skip(line):
                    continue
                code_content_in_line = self.rm_comments_white_space(line)
                # Process code_content_in_line
                tokens_from_line = self.get_tokens_from_code(code_content_in_line)
                print(code_content_in_line)

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
        
    def get_tokens_from_code(self, code_content_in_line):
        pass

    def rm_comments_white_space(self, line):
        """Removes all white space and comments start with //"""
        return line.split('//')[0].strip()

    def write_output(self):
        with open(self.out_file, 'w', encoding='utf_8') as outf:
            pass

