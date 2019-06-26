import os.path as path

class SymbolTable():
    """SymbolTable: Keeps a correspondence between symbolic labels and numeric addresses."""
    def __init__(self):
        """Get the code_contents and creates a new empty symbol table"""
        self.symbol_table = {}
        self.add_predefined_symbols()

    def add_predefined_symbols(self):
        """Initialize the symbol table with all the predefined symbols and their pre-allocated RAM addresses"""
        cwd = path.dirname(path.realpath(__file__))
        predefined_symbol_file = path.join(cwd, 'predefined.symbols')
        with open(predefined_symbol_file, 'r', encoding='utf_8') as inf:
            for line in inf:
                symbol, RAM_address = line.strip().split('\t')
                self.symbol_table[symbol] = RAM_address

    def add_entry(self, symbol, address):
        """Adds the pair (symbol, address) to the table"""
        self.symbol_table[symbol] = address

    def contains(self, symbol):
        """Does the symbol table contain the given symbol?"""
        return symbol in self.symbol_table

    def get_address(self, symbol):
        """Returns the address associated with the symbol."""
        return self.symbol_table[symbol]
