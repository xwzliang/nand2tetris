class SymbolTable:
    """
    SymbolTable: Provides a symbol table abstraction. The symbol table associates the identifier names found in the program with identifier properties needed for compilation: type, kind, and running index. The symbol table for Jack programs has two nested scopes (class/subroutine).
    """
    def __init__(self):
        """Creates a new empty symbol table."""
        self.symbol_table_class = {}
        self.symbol_table_subroutine = {}

    def start_subroutine(self):
        """Starts a new subroutine scope (i.e., resets the subroutine's symbol table)."""
        self.symbol_table_subroutine = {}

    def define(self, symbol_name, symbol_type, symbol_kind):
        """
        arguments: name (String) type (String) kind (STATIC, FIELD, ARG, or VAR)
        Defines a new identifier of a given name, type, and kind and assigns it a running index. STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
        """
        index = self.count_symbol_by_kind(symbol_kind)
        if symbol_kind in {'STATIC', 'FIELD'}:
            self.symbol_table_class[symbol_name] = [symbol_type, symbol_kind, index]
        else:
            self.symbol_table_subroutine[symbol_name] = [symbol_type, symbol_kind, index]

    def count_symbol_by_kind(self, symbol_kind):
        """
        kind (STATIC, FIELD, ARG, or VAR)
        Returns the number of variables of the given kind already defined in the current scope.
        """
        if symbol_kind in {'STATIC', 'FIELD'}:
            return sum(value[1]==symbol_kind for value in self.symbol_table_class.values())
        else:
            return sum(value[1]==symbol_kind for value in self.symbol_table_subroutine.values())

    def get_symbol_attr(self, symbol_name, attr_num):
        """Returns the attribute of the named identifier in the current scope. The attribute is specified by the integer attr_num. If the identifier is unknown in the current scope, returns NONE."""
        if symbol_name in self.symbol_table_subroutine:
            return self.symbol_table_subroutine[symbol_name][attr_num]
        elif symbol_name in self.symbol_table_class:
            return self.symbol_table_class[symbol_name][attr_num]
        else:
            return None

    def get_symbol_type(self, symbol_name):
        return self.get_symbol_attr(symbol_name, 0)

    def get_symbol_kind(self, symbol_name):
        return self.get_symbol_attr(symbol_name, 1)

    def get_symbol_index(self, symbol_name):
        return self.get_symbol_attr(symbol_name, 2)
