class CompilationEngine:
    """CompilationEngine: Effects the actual compilation output. Gets its input from a JackTokenizer and emits its parsed structure into an output file/stream."""
    def __init__(self, tokens_with_tokenType, out_xml_file):
        self.tokens_with_tokenType = tokens_with_tokenType
        self.out_xml_file = out_xml_file

    def compile(self):
        self.write_output(None)

    def write_output(self, output_for_write):
        with open(self.out_xml_file, 'w', encoding='utf_8') as outf:
            pass
