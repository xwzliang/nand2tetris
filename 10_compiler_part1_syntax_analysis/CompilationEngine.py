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
        new_element.text = ' ' + element_text + ' '

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
        self.compile_classVarDec_or_subroutineDec_or_right_curly_brace()

    def compile_classVarDec_or_subroutineDec_or_right_curly_brace(self):
        token, token_type = self.next_token_and_type()
        if token in {'static', 'field'}:
            self.compile_classVarDec(token_type, token)
            self.compile_classVarDec_or_subroutineDec_or_right_curly_brace()
        elif token in {'constructor', 'function', 'method'}:
            self.compile_subroutineDec(token_type, token)
        elif token == '}':
            self.add_sub_element(self.compiled_output_root, token, token_type)

    def compile_classVarDec(self, token_type, token):
        """
        Compiles a static declaration or a field declaration.
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        """
        compiled_output_class_var_dec = etree.SubElement(self.compiled_output_root, 'classVarDec')
        self.add_sub_element(compiled_output_class_var_dec, token_type, token)
        self.compile_type(compiled_output_class_var_dec)
        self.compile_one_or_more_varName_and_semicolon(compiled_output_class_var_dec)

    def compile_one_or_more_varName_and_semicolon(self, parent):
        self.compile_new_token_ensure_token_type('identifier', parent)
        self.compile_more_varName_or_semicolon(parent)

    def compile_more_varName_or_semicolon(self, parent):
        """If there is more varName, compiles them, else compile semicolon to end var declare"""
        token, token_type = self.next_token_and_type()
        if token == ',':	# More VarName need to add
            self.add_sub_element(parent, token_type, token)	# Add ','
            self.compile_new_token_ensure_token_type('identifier', parent)
            self.compile_more_varName_or_semicolon(parent)
        else:
            assert token == ';'
            self.add_sub_element(parent, token_type, token)	# Add ';'

    def compile_type(self, parent):
        """
        Compiles type for var and add token element to parent.
        type: 'int' | 'char' | 'boolean' | className
        """
        token, token_type = self.compile_new_token(parent)
        assert token in {'int', 'char', 'boolean'} or token_type == 'identifier'

    def compile_void_or_type(self, parent):
        """
        Compiles type or 'void' for var and add token element to parent.
        """
        token, token_type = self.compile_new_token(parent)
        assert token in {'void', 'int', 'char', 'boolean'} or token_type == 'identifier'

    def compile_subroutineDec(self, token_type, token):
        """
        Compiles a complete method, function, or constructor.
        subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        """
        compiled_output_subroutineDec = etree.SubElement(self.compiled_output_root, 'subroutineDec')
        # Add token in {'constructor', 'function', 'method'} to compiled_output_subroutineDec
        self.add_sub_element(compiled_output_subroutineDec, token_type, token)
        self.compile_void_or_type(compiled_output_subroutineDec)
        # subroutineName
        self.compile_new_token_ensure_token_type('identifier', compiled_output_subroutineDec)
        self.compile_new_token_ensure_token('(', compiled_output_subroutineDec)
        # parameterList
        compiled_output_parameterList = etree.SubElement(compiled_output_subroutineDec, 'parameterList')
        token, token_type = self.next_token_and_type()
        if token == ')':	# No parameter need to add
            compiled_output_parameterList.text = '\n\t'	# change the print format of empty element compiled_output_parameterList
            self.add_sub_element(compiled_output_subroutineDec, token_type, token)	# Add ')'
        else:	# There is at least one parameter needs to be added
            # type
            assert token in {'int', 'char', 'boolean'} or token_type == 'identifier'
            self.add_sub_element(compiled_output_parameterList, token_type, token)	# Add type
            # varName
            self.compile_new_token_ensure_token_type('identifier', compiled_output_parameterList)
            # more paremeters or ')'
            self.compile_more_parameter_or_right_parenthese(compiled_output_subroutineDec, compiled_output_parameterList)
        # subroutineBody

    def compile_more_parameter_or_right_parenthese(self, parent_subroutineDec, parent_parameterList):
        token, token_type = self.next_token_and_type()
        if token == ')':	# No parameter need to add
            self.add_sub_element(parent_subroutineDec, token_type, token)	# Add ')'
        else:
            assert token == ','
            self.add_sub_element(parent_parameterList, token_type, token)	# Add ','
            self.compile_type(parent_parameterList)
            self.compile_new_token_ensure_token_type('identifier', parent_parameterList)
            self.compile_more_parameter_or_right_parenthese(parent_subroutineDec, parent_parameterList)

    def write_output(self, compiled_etree):
        # output_for_write.write(open(self.out_xml_file, 'w'), encoding='unicode')
        with open(self.out_xml_file, 'w', encoding='utf_8') as outf:
            outf.write(etree.tounicode(compiled_etree, pretty_print=True))
