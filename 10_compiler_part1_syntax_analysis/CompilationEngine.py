# import xml.etree.ElementTree as etree
from lxml import etree

class CompilationEngine:
    """CompilationEngine: Effects the actual compilation output. Gets its input from a JackTokenizer and emits its parsed structure into an output file/stream."""
    def __init__(self, tokens_with_tokenType, out_xml_file):
        self.tokens_with_tokenType = tokens_with_tokenType
        self.out_xml_file = out_xml_file

    def compile(self):
        compiled_etree = self.compile_tokens()
        self.write_output(compiled_etree)

    def compile_tokens(self):
        self.compiled_output_root = etree.Element('class')
        self.compile_class()
        compiled_etree = etree.ElementTree(self.compiled_output_root)
        return compiled_etree

    def compile_new_token_ensure_token_type(self, correct_token_type, parent):
        token, token_type = self.compile_new_token(parent)
        assert token_type == correct_token_type

    def compile_new_token_ensure_token(self, correct_token, parent):
        token, token_type = self.compile_new_token(parent)
        assert token == correct_token

    def compile_new_token(self, parent):
        token, token_type = self.next_token_and_type()
        self.add_sub_element(parent, token_type, token)
        return token, token_type

    def add_sub_element(self, parent, element_tag, element_text):
        new_element = etree.SubElement(parent, element_tag)
        new_element.text = element_text

    def next_token_and_type(self):
        return self.tokens_with_tokenType.pop(0)

    def compile_class(self):
        """
        Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.compile_new_token_ensure_token('class', self.compiled_output_root)
        self.compile_new_token_ensure_token_type('identifier', self.compiled_output_root)
        self.compile_new_token_ensure_token('{', self.compiled_output_root)
        token, token_type = self.next_token_and_type()
        if token in {'static', 'field'}:
            self.compile_class_var_dec(token, token_type)
        elif token in {'constructor', 'function', 'method'}:
            self.compile_subroutine_dec(token, token_type)
        elif token == '}':
            self.add_sub_element(self.compiled_output_root, token, token_type)

    def compile_class_var_dec(self, token, token_type):
        """
        Compiles a static declaration or a field declaration.
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        """
        pass

    def compile_subroutine_dec(self, token, token_type):
        """
        Compiles a complete method, function, or constructor.
        subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        """
        pass

    def write_output(self, compiled_etree):
        # output_for_write.write(open(self.out_xml_file, 'w'), encoding='unicode')
        with open(self.out_xml_file, 'w', encoding='utf_8') as outf:
            outf.write(etree.tounicode(compiled_etree, pretty_print=True))
