
class Char:

    def __init__(self, char: str, name: str):
        self.char = char
        self.name = name

    def __str__(self):
        return self.char

    def __repr__(self):
        return self.char

    def __eq__(self, other):
        if isinstance(other, Char):
            return self.char == other.char
        return self.char == other
