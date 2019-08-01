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

    def show_next_token_and_type(self):
        return self.tokens_with_tokenType[0]

    def compile_class(self):
        """
        Compiles a complete class.
        class: 'class' className '{' classVarDec* subroutineDec* '}'
        """
        self.compile_new_token_ensure_token('class', self.compiled_output_root)
        self.compile_new_token_ensure_token_type('identifier', self.compiled_output_root)
        self.compile_new_token_ensure_token('{', self.compiled_output_root)
        self.compile_classVarDec()
        self.compile_subroutineDec()
        self.compile_new_token_ensure_token('}', self.compiled_output_root)

    def compile_classVarDec(self):
        """
        Compiles a static declaration or a field declaration.
        classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        """
        token = self.show_next_token()
        if token in {'static', 'field'}:
            compiled_output_class_var_dec = etree.SubElement(self.compiled_output_root, 'classVarDec')
            # Add static or field
            self.compile_new_token(compiled_output_class_var_dec)
            self.compile_type(compiled_output_class_var_dec)
            self.compile_one_or_more_varName(compiled_output_class_var_dec)
            self.compile_new_token_ensure_token(';', compiled_output_class_var_dec)
            # Recursive call
            self.compile_classVarDec()

    def compile_one_or_more_varName(self, parent):
        self.compile_new_token_ensure_token_type('identifier', parent)
        self.compile_more_varName_if_exist(parent)

    def compile_more_varName_if_exist(self, parent):
        """If there is more varName, compiles them, else compile semicolon to end var declare"""
        token = self.show_next_token()
        if token == ',':	# More VarName need to add
            self.compile_new_token(parent)	# Add ','
            self.compile_new_token_ensure_token_type('identifier', parent)
            # Recursive call
            self.compile_more_varName_if_exist(parent)

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

    def compile_subroutineDec(self):
        """
        Compiles a complete method, function, or constructor.
        subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        """
        token = self.show_next_token()
        if token in {'constructor', 'function', 'method'}:
            compiled_output_subroutineDec = etree.SubElement(self.compiled_output_root, 'subroutineDec')
            # Add token in {'constructor', 'function', 'method'} to compiled_output_subroutineDec
            self.compile_new_token(compiled_output_subroutineDec)
            self.compile_void_or_type(compiled_output_subroutineDec)
            # subroutineName
            self.compile_new_token_ensure_token_type('identifier', compiled_output_subroutineDec)
            self.compile_new_token_ensure_token('(', compiled_output_subroutineDec)
            # parameterList
            compiled_output_parameterList = etree.SubElement(compiled_output_subroutineDec, 'parameterList')
            token, token_type = self.show_next_token_and_type()
            if token == ')':	# No parameter need to add
                compiled_output_parameterList.text = '\n\t'	# change the print format of empty element compiled_output_parameterList
            else:	# There is at least one parameter needs to be added
                # type
                assert token in {'int', 'char', 'boolean'} or token_type == 'identifier'
                self.compile_new_token(compiled_output_parameterList)	# Add type
                # varName
                self.compile_new_token_ensure_token_type('identifier', compiled_output_parameterList)
                # more paremeters
                self.compile_more_parameter(compiled_output_parameterList)
            self.compile_new_token_ensure_token(')', compiled_output_subroutineDec)
            # subroutineBody
            # subroutineBody: '{' varDec* statements '}'
            compiled_output_subroutineBody = etree.SubElement(compiled_output_subroutineDec, 'subroutineBody')
            self.compile_new_token_ensure_token('{', compiled_output_subroutineBody)
            self.compile_varDec(compiled_output_subroutineBody)
            compiled_output_statements = etree.SubElement(compiled_output_subroutineBody, 'statements')
            self.compile_statements(compiled_output_statements)
            self.compile_new_token_ensure_token('}', compiled_output_subroutineBody)
            # Recursive call
            self.compile_subroutineDec()

    def compile_more_parameter(self, parent):
        token = self.show_next_token()
        if token == ',':	# More parameter need to add
            self.compile_new_token(parent)	# Add ','
            self.compile_type(parent)
            self.compile_new_token_ensure_token_type('identifier', parent)
            # Recursive call
            self.compile_more_parameter(parent)

    def compile_varDec(self, parent):
        """varDec: 'var' type varName (',' varName)* ';'"""
        token = self.show_next_token()
        if token == 'var':
            compiled_output_varDec = etree.SubElement(parent, 'varDec')
            self.compile_new_token(compiled_output_varDec)	# Add 'var'
            self.compile_type(compiled_output_varDec)
            self.compile_new_token_ensure_token_type('identifier', compiled_output_varDec)
            self.compile_more_varName_if_exist(compiled_output_varDec)
            self.compile_new_token_ensure_token(';', compiled_output_varDec)
            # Recursive call
            self.compile_varDec(parent)

    def compile_statements(self, parent):
        """statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement"""
        token = self.show_next_token()
        if token in {'let', 'if', 'while', 'do', 'return'}:
            if token == 'let':
                self.compile_statement_let(parent)
            elif token == 'if':
                self.compile_statement_if(parent)
            elif token == 'while':
                self.compile_statement_while(parent)
            elif token == 'do':
                self.compile_statement_do(parent)
            else:	# return
                self.compile_statement_return(parent)
            # Recursive call
            self.compile_statements(parent)

    def compile_statement_let(self, parent):
        """
        letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
        """
        compiled_output_statement = etree.SubElement(parent, 'letStatement')
        self.compile_new_token_ensure_token('let', compiled_output_statement)
        # varName
        self.compile_new_token_ensure_token_type('identifier', compiled_output_statement)
        token = self.show_next_token()
        if token == '[':
            self.compile_new_token(compiled_output_statement)	# Add '['
            self.compile_expression(compiled_output_statement)
            self.compile_new_token_ensure_token(']', compiled_output_statement)
        self.compile_new_token_ensure_token('=', compiled_output_statement)	# Add '='
        self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_statement_if(self, parent):
        """
        ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        """
        compiled_output_statement= etree.SubElement(parent, 'ifStatement')
        self.compile_new_token_ensure_token('if', compiled_output_statement)
        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token('{', compiled_output_statement)
        compiled_output_statements_if = etree.SubElement(compiled_output_statement, 'statements')
        self.compile_statements(compiled_output_statements_if)
        self.compile_new_token_ensure_token('}', compiled_output_statement)
        next_token = self.show_next_token()
        if next_token == 'else':
            self.compile_new_token_ensure_token('else', compiled_output_statement)
            self.compile_new_token_ensure_token('{', compiled_output_statement)
            compiled_output_statements_else = etree.SubElement(compiled_output_statement, 'statements')
            self.compile_statements(compiled_output_statements_else)
            self.compile_new_token_ensure_token('}', compiled_output_statement)

    def compile_statement_while(self, parent):
        """
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        """
        compiled_output_statement= etree.SubElement(parent, 'whileStatement')
        self.compile_new_token_ensure_token('while', compiled_output_statement)
        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expression(compiled_output_statement)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token('{', compiled_output_statement)
        compiled_output_statements_while = etree.SubElement(compiled_output_statement, 'statements')
        self.compile_statements(compiled_output_statements_while)
        self.compile_new_token_ensure_token('}', compiled_output_statement)

    def compile_statement_do(self, parent):
        """
        doStatement: 'do' subroutineCall ';'
        """
        compiled_output_statement= etree.SubElement(parent, 'doStatement')
        self.compile_new_token_ensure_token('do', compiled_output_statement)
        # subroutineCall
        self.compile_subroutineCall(compiled_output_statement)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_subroutineCall(self, parent):
        """
        subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        """
        self.compile_new_token_ensure_token_type('identifier', parent)	# subroutineName or className or varName
        next_token = self.show_next_token()
        if next_token == '.':
            self.compile_new_token_ensure_token('.', parent)
            self.compile_new_token_ensure_token_type('identifier', parent)	# subroutineName

        self.compile_new_token_ensure_token('(', parent)
        self.compile_expressionList(parent)
        self.compile_new_token_ensure_token(')', parent)

    def compile_statement_return(self, parent):
        """
        ReturnStatement 'return' expression? ';'
        """
        compiled_output_statement= etree.SubElement(parent, 'returnStatement')
        self.compile_new_token_ensure_token('return', compiled_output_statement)
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
        """
        term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
        """
        compiled_output_term = etree.SubElement(parent, 'term')
        next_token, token_type = self.show_next_token_and_type()
        if token_type == 'integerConstant' or next_token in {'true', 'false', 'null', 'this'}:	# integerConstant or keywordConstant
            self.compile_new_token(compiled_output_term)
        elif token_type == 'stringConstant':
            token, token_type = self.next_token_and_type()
            # remove dowble quote symbol in token
            self.add_sub_element(compiled_output_term, token_type, token[1:-1])
        elif token_type == 'identifier':
            next_token, token_type = self.tokens_with_tokenType[1]
            if next_token == '[':
                self.compile_new_token_ensure_token_type('identifier', compiled_output_term)
                self.compile_new_token_ensure_token('[', compiled_output_term)
                self.compile_expression(compiled_output_term)
                self.compile_new_token_ensure_token(']', compiled_output_term)
            elif next_token == '(' or next_token == '.':
                self.compile_subroutineCall(compiled_output_term)
            else:	# A single varName
                self.compile_new_token_ensure_token_type('identifier', compiled_output_term)
        elif next_token == '(':
            self.compile_new_token(compiled_output_term)
            self.compile_expression(compiled_output_term)
            self.compile_new_token_ensure_token(')', compiled_output_term)
        elif next_token in {'-', '~'}:	# unaryOp
            self.compile_new_token(compiled_output_term)
            self.compile_term(compiled_output_term)
        else:
            raise 'Not a valid expression'

    def compile_zero_or_more_op_and_term(self, parent):
        """
        op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        """
        next_token = self.show_next_token()
        if next_token in {'+', '-', '*', '/', '&', '|', '<', '>', '='}:	# in op
            self.compile_new_token(parent)	# add op
            self.compile_term(parent)
            # Recursive call
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
        else:
            self.compile_expression(compiled_output_expressionList)
            self.compile_comma_and_expression(compiled_output_expressionList)

    def compile_comma_and_expression(self, parent):
        next_token = self.show_next_token()
        if next_token == ',':
            self.compile_new_token_ensure_token(',', parent)
            self.compile_expression(parent)
            # Recursive call
            self.compile_comma_and_expression(parent)

    def write_output(self, compiled_etree):
        with open(self.out_xml_file, 'w', encoding='utf_8') as outf:
            outf.write(etree.tounicode(compiled_etree, pretty_print=True))
