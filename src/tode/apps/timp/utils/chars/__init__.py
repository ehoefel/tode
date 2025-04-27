from .unicode import Unicode
from .nerd_fonts import NerdFonts


class Chars:

    def get_block_names(cls=None):
        return Unicode.get_block_names() + NerdFonts.get_block_names()

    def get_block_chars(block_name: str):
        if block_name in NerdFonts.get_block_names():
            return NerdFonts.get_block_chars(block_name)
        if block_name in Unicode.get_block_names():
            return Unicode.get_block_chars(block_name)
        return []
