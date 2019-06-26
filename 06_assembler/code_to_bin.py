import os.path as path

class Code2Bin():
    """Translates Hack assembly language mnemonics into binary codes"""
    def __init__(self):
        """Build dict for translations"""
        self.comp_dict = self.build_bin_dict('comp.code2bin')
        self.dest_dict = self.build_bin_dict('dest.code2bin')
        self.jump_dict = self.build_bin_dict('jump.code2bin')

    def build_bin_dict(self, data_file):
        """Read the contents of the data_file into bin_dict"""
        bin_dict = {}
        with open(path.join(path.dirname(path.realpath(__file__)), data_file), 'r', encoding='utf_8') as dataf:
            for line in dataf:
                command = line.strip().split('\t')[0]
                binary = line.strip().split('\t')[1]
                bin_dict[command] = binary
        return bin_dict

    def comp2bin(self, code):
        """Returns the binary code of the comp mnemonic."""
        return self.comp_dict[code]

    def dest2bin(self, code):
        """Returns the binary code of the dest mnemonic."""
        return self.dest_dict[code]

    def jump2bin(self, code):
        """Returns the binary code of the jump mnemonic."""
        return self.jump_dict[code]

