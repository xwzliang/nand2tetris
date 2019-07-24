class JackTokenizer:
    """JackTokenizer: Removes all comments and white space from the input stream and breaks it into Jack-language tokens, as specified by the Jack grammar"""
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file

    def write_output(self):
        with open(self.out_file, 'w', encoding='utf_8') as outf:
            pass

    def tokenize(self):
        self.write_output()
