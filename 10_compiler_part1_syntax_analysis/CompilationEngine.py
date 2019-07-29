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
        assert token_type == correct_token_type, '{} with token_type {} not expected'.format(token, token_type)

    def compile_new_token_ensure_token(self, correct_token, parent):
        token, token_type = self.compile_new_token(parent)
        assert token == correct_token, '{} with token_type {} not expected'.format(token, token_type)

    def compile_new_token(self, parent):
        token, token_type = self.next_token_and_type()
        self.add_sub_element(parent, token_type, token)
        return token, token_type

    def add_sub_element(self, parent, element_tag, element_text):
        new_element = etree.SubElement(parent, element_tag)
        new_element.text = ' ' + element_text + ' '

    def next_token_and_type(self):
        return self.tokens_with_tokenType.pop(0)

    def show_next_token(self):
        token, token_type = self.tokens_with_tokenType[0]
        return token

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
            self.compile_subroutineDec_or_right_curly_brace()
        elif token == '}':
            self.add_sub_element(self.compiled_output_root, token_type, token)

    def compile_subroutineDec_or_right_curly_brace(self):
        token, token_type = self.next_token_and_type()
        if token in {'constructor', 'function', 'method'}:
            self.compile_subroutineDec(token_type, token)
            self.compile_subroutineDec_or_right_curly_brace()
        elif token == '}':
            self.add_sub_element(self.compiled_output_root, token_type, token)


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
        # subroutineBody: '{' varDec* statements '}'
        compiled_output_subroutineBody = etree.SubElement(compiled_output_subroutineDec, 'subroutineBody')
        self.compile_new_token_ensure_token('{', compiled_output_subroutineBody)
        token, token_type = self.next_token_and_type()
        if token == 'var':
            self.compile_varDec_and_statements_or_right_curly_brace(compiled_output_subroutineBody, token_type, token)
        elif token == '}':
            self.add_sub_element(compiled_output_subroutineBody, token_type, token)	# Add '}'
        else:	# statements
            compiled_output_statements = etree.SubElement(compiled_output_subroutineBody, 'statements')
            self.compile_statements_and_right_curly_brace(compiled_output_subroutineBody, compiled_output_statements, token_type, token)

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

    def compile_varDec_and_statements_or_right_curly_brace(self, parent, token_type, token):
        """varDec: 'var' type varName (',' varName)* ';'"""
        compiled_output_varDec = etree.SubElement(parent, 'varDec')
        self.add_sub_element(compiled_output_varDec, token_type, token)	# Add 'var'
        self.compile_type(compiled_output_varDec)
        self.compile_new_token_ensure_token_type('identifier', compiled_output_varDec)
        self.compile_more_varName_or_semicolon(compiled_output_varDec)
        token, token_type = self.next_token_and_type()
        if token == 'var':
            self.compile_varDec_and_statements_or_right_curly_brace(parent, token_type, token)
        elif token == '}':
            self.add_sub_element(parent, token_type, token)	# Add '}'
        else:	# statements
            compiled_output_statements = etree.SubElement(parent, 'statements')
            self.compile_statements_and_right_curly_brace(parent, compiled_output_statements, token_type, token)

    def compile_statements_and_right_curly_brace(self, grandparent, parent, token_type, token):
        """statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement"""
        assert token in {'let', 'if', 'while', 'do', 'return'}, '{} is not correct'.format(token)
        if token == 'let':
            self.compile_statement_let(parent, token_type, token)
        elif token == 'if':
            self.compile_statement_if(parent, token_type, token)
        elif token == 'while':
            self.compile_statement_while(parent, token_type, token)
        elif token == 'do':
            self.compile_statement_do(parent, token_type, token)
        else:	# return
            self.compile_statement_return(parent, token_type, token)
        token, token_type = self.next_token_and_type()
        if token == '}':
            self.add_sub_element(grandparent, token_type, token)	# Add '}'
        else:	# More statements to be added
            self.compile_statements_and_right_curly_brace(grandparent, parent, token_type, token)

    def compile_zero_or_more_statements_and_right_curly_brace(self, grandparent, parent):
        token, token_type = self.next_token_and_type()
        if token == '}':
            self.add_sub_element(grandparent, token_type, token)	# Add '}'
        else:	# More statements to be added
            self.compile_statements_and_right_curly_brace(grandparent, parent, token_type, token)

    def compile_statement_let(self, parent, token_type, token):
        """
        letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        """
        compiled_output_statement = etree.SubElement(parent, 'letStatement')
        self.add_sub_element(compiled_output_statement, token_type, token)	# Add 'let'
        # varName
        self.compile_new_token_ensure_token_type('identifier', compiled_output_statement)
        token, token_type = self.next_token_and_type()
        if token == '[':
            self.add_sub_element(compiled_output_statement, token_type, token)	# Add '['
            self.compile_expression(compiled_output_statement)
            self.compile_new_token_ensure_token(']', compiled_output_statement)
            token, token_type = self.next_token_and_type()
        assert token == '='
        self.add_sub_element(compiled_output_statement, token_type, token)	# Add '='
        self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_statement_if(self, parent, token_type, token):
        """
        ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        compiled_output_statement= etree.SubElement(parent, 'ifStatement')
        self.add_sub_element(compiled_output_statement, token_type, token)	# Add 'if'
        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token('{', compiled_output_statement)
        compiled_output_statements_if = etree.SubElement(compiled_output_statement, 'statements')
        self.compile_zero_or_more_statements_and_right_curly_brace(compiled_output_statement, compiled_output_statements_if)
        next_token = self.show_next_token()
        if next_token == 'else':
            self.compile_new_token_ensure_token('else', compiled_output_statement)
            self.compile_new_token_ensure_token('{', compiled_output_statement)
            compiled_output_statements_else = etree.SubElement(compiled_output_statement, 'statements')
            self.compile_zero_or_more_statements_and_right_curly_brace(compiled_output_statement, compiled_output_statements_else)

    def compile_statement_while(self, parent, token_type, token):
        """
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        compiled_output_statement= etree.SubElement(parent, 'whileStatement')
        self.add_sub_element(compiled_output_statement, token_type, token)	# Add 'while'
        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token('{', compiled_output_statement)
        compiled_output_statements_while = etree.SubElement(compiled_output_statement, 'statements')
        self.compile_zero_or_more_statements_and_right_curly_brace(compiled_output_statement, compiled_output_statements_while)

    def compile_statement_do(self, parent, token_type, token):
        """
        doStatement: 'do' subroutineCall ';'
        """
        compiled_output_statement= etree.SubElement(parent, 'doStatement')
        self.add_sub_element(compiled_output_statement, token_type, token)	# Add 'do'
        # subroutineCall
        # subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        self.compile_new_token_ensure_token_type('identifier', compiled_output_statement)	# subroutineName or className or varName
        next_token = self.show_next_token()
        if next_token == '.':
            self.compile_new_token_ensure_token('.', compiled_output_statement)
            self.compile_new_token_ensure_token_type('identifier', compiled_output_statement)	# subroutineName

        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expressionList(compiled_output_statement)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_statement_return(self, parent, token_type, token):
        """
        ReturnStatement 'return' expression? ';'
        """
        compiled_output_statement= etree.SubElement(parent, 'returnStatement')
        self.add_sub_element(compiled_output_statement, token_type, token)	# Add 'return'
        next_token = self.show_next_token()
        if next_token != ';':	# has expression
            self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_expression(self, parent):
        """
        expression: term (op term)*
        """
        compiled_output_expression = etree.SubElement(parent, 'expression')
        self.compile_term(compiled_output_expression)
        self.compile_zero_or_more_op_and_term(compiled_output_expression)

    def compile_term(self, parent):
        compiled_output_term = etree.SubElement(parent, 'term')
        # Simplify the situation first: only one token added
        self.compile_new_token(compiled_output_term)

    def compile_zero_or_more_op_and_term(self, parent):
        """
        op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        """
        next_token = self.show_next_token()
        if next_token in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:	# in op
            self.compile_new_token(parent)	# add op
            self.compile_term(parent)
            self.compile_zero_or_more_op_and_term(parent)

    def compile_expressionList(self, parent):
        """
        expressionList: (expression (',' expression)* )?
        """
        compiled_output_expressionList = etree.SubElement(parent, 'expressionList')
        next_token = self.show_next_token()
        if next_token == ')':
            # No expression
            compiled_output_expressionList.text = '\n\t'
            return
        else:
            self.compile_expression(compiled_output_expressionList)
            self.compile_comma_and_expression(compiled_output_expressionList)

    def compile_comma_and_expression(self, parent):
        next_token = self.show_next_token()
        if next_token == ',':
            self.compile_new_token_ensure_token(',', parent)
            self.compile_expression(parent)
            self.compile_comma_and_expression(parent)

    def write_output(self, compiled_etree):
        # output_for_write.write(open(self.out_xml_file, 'w'), encoding='unicode')
        with open(self.out_xml_file, 'w', encoding='utf_8') as outf:
            outf.write(etree.tounicode(compiled_etree, pretty_print=True))
