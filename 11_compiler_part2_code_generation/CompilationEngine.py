# import xml.etree.ElementTree as etree
from lxml import etree

from SymbolTable import SymbolTable
from VMWriter import VMWriter

class CompilationEngine:
    """CompilationEngine: Effects the actual compilation output. Gets its input from a JackTokenizer and emits its parsed structure into an output file/stream."""
    def __init__(self, tokens_with_tokenType, out_vm_file):
        self.tokens_with_tokenType = tokens_with_tokenType
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(out_vm_file)
        self.class_name = out_vm_file.stem
        self.construct_op_dict()
        self.construct_segment_dict()
        self.while_label_index = 0
        self.if_else_label_index = 0

    def construct_op_dict(self):
        self.op_dict = {
                '+': 'add',
                '-': 'sub',
                '&': 'and',
                '|': 'or',
                '<': 'lt',
                '>': 'gt',
                '=': 'eq',
                }

    def construct_segment_dict(self):
        """Translate the kind of variable to related memory segment name"""
        self.segment_dict = {
                'STATIC': 'static',
                'FIELD': 'this',
                'ARG': 'argument',
                'VAR': 'local',
                }

    def compile(self):
        compiled_etree = self.compile_tokens()
        # Uncomment following line if you want to see the output of compiled element tree
        # print(etree.tounicode(compiled_etree, pretty_print=True))
        self.vm_writer.close()

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
            symbol_kind = token.upper()
            # Add static or field
            self.compile_new_token(compiled_output_class_var_dec)
            symbol_type = self.compile_type(compiled_output_class_var_dec)
            self.compile_one_or_more_varName(compiled_output_class_var_dec, symbol_type, symbol_kind)
            self.compile_new_token_ensure_token(';', compiled_output_class_var_dec)
            # Recursive call
            self.compile_classVarDec()

    def compile_one_or_more_varName(self, parent, symbol_type, symbol_kind):
        self.add_new_symbol(symbol_type, symbol_kind)
        self.compile_new_token_ensure_token_type('identifier', parent)
        self.compile_more_varName_if_exist(parent, symbol_type, symbol_kind)

    def add_new_symbol(self, symbol_type, symbol_kind):
        """Next token is symbol_name, add this symbol_name and its symbol_type and symbol_kind to self.symbol_table"""
        symbol_name = self.show_next_token()
        self.symbol_table.define(symbol_name, symbol_type, symbol_kind)

    def compile_more_varName_if_exist(self, parent, symbol_type, symbol_kind):
        """If there is more varName, compiles them"""
        token = self.show_next_token()
        if token == ',':	# More VarName need to add
            self.compile_new_token(parent)	# Add ','
            self.add_new_symbol(symbol_type, symbol_kind)
            self.compile_new_token_ensure_token_type('identifier', parent)
            # Recursive call
            self.compile_more_varName_if_exist(parent, symbol_type, symbol_kind)

    def compile_type(self, parent):
        """
        Compiles type for var and add token element to parent.
        type: 'int' | 'char' | 'boolean' | className
        """
        token, token_type = self.compile_new_token(parent)
        assert token in {'int', 'char', 'boolean'} or token_type == 'identifier'
        return token

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
            self.symbol_table.start_subroutine()	# Reset the subroutine's symbol table
            function_kind = token
            compiled_output_subroutineDec = etree.SubElement(self.compiled_output_root, 'subroutineDec')
            # Add token in {'constructor', 'function', 'method'} to compiled_output_subroutineDec
            self.compile_new_token(compiled_output_subroutineDec)
            self.compile_void_or_type(compiled_output_subroutineDec)
            # subroutineName
            function_name = self.class_name + '.' + self.show_next_token()
            self.compile_new_token_ensure_token_type('identifier', compiled_output_subroutineDec)
            self.compile_new_token_ensure_token('(', compiled_output_subroutineDec)
            # parameterList
            if function_kind == 'method':
                # this is a dummy symbol added to the symbol_table's ARG, for the side effect that method's number of arguments will add 1. A method with k arguments operates on k+1 arguments actually, and the first argument (argument number 0) always refers to the this object
                self.symbol_table.define('this', 'int', 'ARG')
            self.compile_parameterList(compiled_output_subroutineDec)
            self.compile_new_token_ensure_token(')', compiled_output_subroutineDec)
            # subroutineBody
            self.compile_subroutineBody(compiled_output_subroutineDec, function_name, function_kind)

            # Recursive call
            self.compile_subroutineDec()

    def compile_parameterList(self, parent):
        """
        ((type varName) (',' type varName)*)?
        """
        compiled_output_parameterList = etree.SubElement(parent, 'parameterList')
        token, token_type = self.show_next_token_and_type()
        if token == ')':	# No parameter need to add
            compiled_output_parameterList.text = '\n\t'	# change the print format of empty element compiled_output_parameterList
        else:	# There is at least one parameter needs to be added
            # type
            assert token in {'int', 'char', 'boolean'} or token_type == 'identifier'
            symbol_kind = 'ARG'
            symbol_type = token
            self.compile_new_token(compiled_output_parameterList)	# Add type
            self.add_new_symbol(symbol_type, symbol_kind)
            # varName
            self.compile_new_token_ensure_token_type('identifier', compiled_output_parameterList)
            # more paremeters
            self.compile_more_parameter(compiled_output_parameterList)

    def compile_subroutineBody(self, parent, function_name, function_kind):
        """
        subroutineBody: '{' varDec* statements '}'
        """
        compiled_output_subroutineBody = etree.SubElement(parent, 'subroutineBody')
        self.compile_new_token_ensure_token('{', compiled_output_subroutineBody)
        self.compile_varDec(compiled_output_subroutineBody)
        local_vars_num = self.symbol_table.count_symbol_by_kind('VAR')
        self.vm_writer.write_function(function_name, local_vars_num)
        if function_kind == 'constructor':
            # translate this=Memory.alloc(fields_num)
            fields_num = self.symbol_table.count_symbol_by_kind('FIELD')
            self.vm_writer.write_push('constant', fields_num)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('pointer', 0)
        elif function_kind == 'method':
            # Point the virtual this segment to the current object (using pointer 0)
            self.vm_writer.write_push('argument', 0)	# In method, this object address will always be stored in the first argument
            self.vm_writer.write_pop('pointer', 0)
        compiled_output_statements = etree.SubElement(compiled_output_subroutineBody, 'statements')
        self.compile_statements(compiled_output_statements)
        self.compile_new_token_ensure_token('}', compiled_output_subroutineBody)

    def compile_more_parameter(self, parent):
        token = self.show_next_token()
        if token == ',':	# More parameter need to add
            self.compile_new_token(parent)	# Add ','
            symbol_kind = 'ARG'
            symbol_type = self.compile_type(parent)
            self.add_new_symbol(symbol_type, symbol_kind)
            self.compile_new_token_ensure_token_type('identifier', parent)
            # Recursive call
            self.compile_more_parameter(parent)

    def compile_varDec(self, parent):
        """varDec: 'var' type varName (',' varName)* ';'"""
        token = self.show_next_token()
        if token == 'var':
            compiled_output_varDec = etree.SubElement(parent, 'varDec')
            symbol_kind = token.upper()
            self.compile_new_token(compiled_output_varDec)	# Add 'var'
            symbol_type = self.compile_type(compiled_output_varDec)
            self.add_new_symbol(symbol_type, symbol_kind)
            self.compile_new_token_ensure_token_type('identifier', compiled_output_varDec)
            self.compile_more_varName_if_exist(compiled_output_varDec, symbol_type, symbol_kind)
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
        vm: pop the value of expression to varName
        """
        compiled_output_statement = etree.SubElement(parent, 'letStatement')
        self.compile_new_token_ensure_token('let', compiled_output_statement)
        # varName
        symbol_name = self.show_next_token()
        self.compile_new_token_ensure_token_type('identifier', compiled_output_statement)
        token = self.show_next_token()
        if token == '[':	# Array
            """
            code:
                arr[expression1] = expression2
            vm:
            	push arr
                push expression1
                add
                push expression2
                pop temp 0
                pop pointer 1
                push temp 0
                pop that 0
            The reason to use temp 0 and delayed pop pointer 1 after push expression2 is that expression2 may also contain arrays, for example: a[i]=b[j], then the value in pointer 1 will mess up. So we must pop the returned value by expression2 to temp 0 for the rescue.
            """
            self.write_push_variable(symbol_name)
            self.compile_new_token(compiled_output_statement)	# Add '['
            self.compile_expression(compiled_output_statement)
            self.vm_writer.write_arithmetic('add')
            self.compile_new_token_ensure_token(']', compiled_output_statement)
        self.compile_new_token_ensure_token('=', compiled_output_statement)	# Add '='
        self.compile_expression(compiled_output_statement)
        if token == '[':	# Array
            # Array assignment always first align that to the address to be modified, then "pop that 0"
            self.vm_writer.write_pop('temp', 0)
            self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_push('temp', 0)
            self.vm_writer.write_pop('that', 0)
        else:	# a varName
            self.write_pop_variable(symbol_name)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_statement_if(self, parent):
        """
        ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
        code:
        	if (cond)
                    s1
                else
                    s2
        vm:
        	VM code for computing ~(cond)
                if-goto L1
                VM code for executing s1
                goto L2
                label L1
                VM code for executing s2
                label L2
        """
        compiled_output_statement= etree.SubElement(parent, 'ifStatement')
        self.compile_new_token_ensure_token('if', compiled_output_statement)
        self.if_else_label_index += 1
        else_start_label_name = 'ELSE_START_{}_{}'.format(self.class_name.upper(), self.if_else_label_index) 
        if_else_end_label_name = 'IF_ELSE_END_{}_{}'.format(self.class_name.upper(), self.if_else_label_index) 
        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expression(compiled_output_statement)
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if_goto(else_start_label_name)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token('{', compiled_output_statement)
        compiled_output_statements_if = etree.SubElement(compiled_output_statement, 'statements')
        self.compile_statements(compiled_output_statements_if)
        self.vm_writer.write_goto(if_else_end_label_name)
        self.compile_new_token_ensure_token('}', compiled_output_statement)
        self.vm_writer.write_label(else_start_label_name)
        next_token = self.show_next_token()
        if next_token == 'else':
            self.compile_new_token_ensure_token('else', compiled_output_statement)
            self.compile_new_token_ensure_token('{', compiled_output_statement)
            compiled_output_statements_else = etree.SubElement(compiled_output_statement, 'statements')
            self.compile_statements(compiled_output_statements_else)
            self.compile_new_token_ensure_token('}', compiled_output_statement)
        self.vm_writer.write_label(if_else_end_label_name)

    def compile_statement_while(self, parent):
        """
        whileStatement: 'while' '(' expression ')' '{' statements '}'
        code: 
            while (cond) 
                s1
        vm:
            label L1
            VM code for computing ~(cond)
            if-goto L2
            VM code for executing s1
            goto L1
            label L2
        """
        compiled_output_statement= etree.SubElement(parent, 'whileStatement')
        self.compile_new_token_ensure_token('while', compiled_output_statement)
        self.while_label_index += 1
        while_start_label_name = 'WHILE_START_{}_{}'.format(self.class_name.upper(), self.while_label_index) 
        while_end_label_name = 'WHILE_END_{}_{}'.format(self.class_name.upper(), self.while_label_index) 
        self.vm_writer.write_label(while_start_label_name)
        self.compile_new_token_ensure_token('(', compiled_output_statement)
        self.compile_expression(compiled_output_statement)
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_if_goto(while_end_label_name)
        self.compile_new_token_ensure_token(')', compiled_output_statement)
        self.compile_new_token_ensure_token('{', compiled_output_statement)
        compiled_output_statements_while = etree.SubElement(compiled_output_statement, 'statements')
        self.compile_statements(compiled_output_statements_while)
        self.vm_writer.write_goto(while_start_label_name)
        self.vm_writer.write_label(while_end_label_name)
        self.compile_new_token_ensure_token('}', compiled_output_statement)

    def compile_statement_do(self, parent):
        """
        doStatement: 'do' subroutineCall ';'
        """
        compiled_output_statement= etree.SubElement(parent, 'doStatement')
        self.compile_new_token_ensure_token('do', compiled_output_statement)
        # subroutineCall
        self.compile_subroutineCall(compiled_output_statement)
        # When translating a do sub statement where sub is a void method or function, the caller of the corresponding VM function must pop (and ignore) the returned value (which is always the constant 0).
        self.vm_writer.write_pop('temp', 0)
        self.compile_new_token_ensure_token(';', compiled_output_statement)

    def compile_subroutineCall(self, parent):
        """
        subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
        """
        name = self.show_next_token()
        self.compile_new_token_ensure_token_type('identifier', parent)	# subroutineName or className or varName
        next_token = self.show_next_token()
        if next_token == '.':
            self.compile_new_token_ensure_token('.', parent)
            symbol_type = self.symbol_table.get_symbol_type(name)
            if not symbol_type:
                # Not defined in symbol_table, so name must be className, and function name is simply className.subroutineName, needs not to be changed
                function_name = name + '.' + self.show_next_token()
                args_num_should_add_1 = False
            else:
                # name is varName, so it is an instance of a className, className is symbol_type, so we push the value of the varName first, which is the base address of the class instance, then set the function name to  className.subroutineName
                args_num_should_add_1 = True
                self.write_push_variable(name)
                function_name = symbol_type + '.' + self.show_next_token()
            self.compile_new_token_ensure_token_type('identifier', parent)	# subroutineName
        else:
            # no '.' found, so name is subroutineName, function name should be self.class_name.subroutineName, and we need push this (pointer 0) first
            self.vm_writer.write_push('pointer', 0)
            function_name = self.class_name + '.' + name
            args_num_should_add_1 = True

        self.compile_new_token_ensure_token('(', parent)
        self.compile_expressionList(parent, function_name, args_num_should_add_1)
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
        else:
            # void functions return the constant 0
            self.vm_writer.write_push('constant', 0)
        self.vm_writer.write_return()
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
            if token_type == 'integerConstant':
                self.vm_writer.write_push('constant', next_token)
            elif next_token == 'true':
                # true = -1, which is 16 bit each bit is 1
                self.vm_writer.write_push('constant', 1)
                self.vm_writer.write_arithmetic('neg')
            elif next_token == 'false' or next_token == 'null':
                self.vm_writer.write_push('constant', 0)
            else:	# next_token == 'this'
                # this will always be the content of pointer 0
                self.vm_writer.write_push('pointer', 0)
            self.compile_new_token(compiled_output_term)
        elif token_type == 'stringConstant':
            token, token_type = self.next_token_and_type()
            # remove double quote symbol in token
            string = token[1:-1]
            # Push string using OS String: String.new(length), String.appendChar(nextChar)
            self.vm_writer.write_push('constant', len(string))
            self.vm_writer.write_call('String.new', 1)
            for char in string:
                self.vm_writer.write_push('constant', ord(char))
                self.vm_writer.write_call('String.appendChar', 2)
            self.add_sub_element(compiled_output_term, token_type, string)
        elif token_type == 'identifier':
            next_next_token, token_type = self.tokens_with_tokenType[1]
            if next_next_token == '[':	# Array
                """
                code: 
                    a[i]
                vm:
                    push a
                    push i
                    add
                    pop pointer 1
                    push that 0
                """
                symbol_name = next_token
                self.write_push_variable(symbol_name)
                self.compile_new_token_ensure_token_type('identifier', compiled_output_term)
                self.compile_new_token_ensure_token('[', compiled_output_term)
                self.compile_expression(compiled_output_term)
                self.vm_writer.write_arithmetic('add')
                self.vm_writer.write_pop('pointer', 1)
                # Push the value of the array item to stack using segment that
                self.vm_writer.write_push('that', 0)
                self.compile_new_token_ensure_token(']', compiled_output_term)
            elif next_next_token == '(' or next_next_token == '.':
                self.compile_subroutineCall(compiled_output_term)
            else:	# A single varName
                symbol_name = next_token
                self.write_push_variable(symbol_name)
                self.compile_new_token_ensure_token_type('identifier', compiled_output_term)
        elif next_token == '(':
            self.compile_new_token(compiled_output_term)
            self.compile_expression(compiled_output_term)
            self.compile_new_token_ensure_token(')', compiled_output_term)
        elif next_token in {'-', '~'}:	# unaryOp
            self.compile_new_token(compiled_output_term)
            self.compile_term(compiled_output_term)
            if next_token == '-':
                self.vm_writer.write_arithmetic('neg')
            else:
                self.vm_writer.write_arithmetic('not')
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
            # Write vm code for operator
            if next_token == '*':
                self.vm_writer.write_call('Math.multiply', 2)
            elif next_token == '/':
                self.vm_writer.write_call('Math.divide', 2)
            else:
                operator = self.op_dict[next_token]
                self.vm_writer.write_arithmetic(operator)
            # Recursive call
            self.compile_zero_or_more_op_and_term(parent)

    def compile_expressionList(self, parent, function_name, args_num_should_add_1):
        """
        expressionList: (expression (',' expression)* )?
        """
        compiled_output_expressionList = etree.SubElement(parent, 'expressionList')
        self.args_num = 0
        if args_num_should_add_1:
            # if function_name is varName.subroutineName or self.class_name.subroutineName, the number of arguments should add 1 because we first push the base address of the operated object
            self.args_num += 1
        next_token = self.show_next_token()
        if next_token == ')':
            # No expression
            compiled_output_expressionList.text = '\n\t'
            self.vm_writer.write_call(function_name, self.args_num)
        else:
            self.compile_expression(compiled_output_expressionList)
            self.args_num += 1
            self.compile_comma_and_expression(compiled_output_expressionList)
            self.vm_writer.write_call(function_name, self.args_num)

    def compile_comma_and_expression(self, parent):
        next_token = self.show_next_token()
        if next_token == ',':
            self.compile_new_token_ensure_token(',', parent)
            self.args_num += 1
            self.compile_expression(parent)
            # Recursive call
            self.compile_comma_and_expression(parent)

    def write_push_variable(self, symbol_name):
        """Push the value of variable to working stack"""
        index = self.symbol_table.get_symbol_index(symbol_name)
        symbol_kind = self.symbol_table.get_symbol_kind(symbol_name)
        segment = self.segment_dict[symbol_kind]
        self.vm_writer.write_push(segment, index)

    def write_pop_variable(self, symbol_name):
        """Pop the top value of the working stack to variable"""
        index = self.symbol_table.get_symbol_index(symbol_name)
        symbol_kind = self.symbol_table.get_symbol_kind(symbol_name)
        segment = self.segment_dict[symbol_kind]
        self.vm_writer.write_pop(segment, index)
