# cSpell:disable

from rich.style import Style as RichStyle
from rich.segment import Segment

from textual.color import Color


class Pixel:

    BLANK = " "
    fg: Color

    def __init__(
        self,
        char: str,
        fg: Color | None = None,
        bg: Color | None = None,
    ) -> None:
        super().__init__()
        self.char = char
        self.fg = fg
        self.bg = bg

    @property
    def style(self) -> RichStyle:
        kwargs = dict()
        if self.fg is not None:
            fg = self.fg
            kwargs['color'] = fg.rich_color
        if self.bg is not None:
            bg = self.bg
            kwargs['bgcolor'] = bg.rich_color
        return RichStyle(**kwargs)

    @property
    def segment(self) -> Segment:
        return Segment(self.char, self.style)

    def clone(self):
        return Pixel(self.char, self.fg, self.bg)

    def is_blank(self):
        return (
            self.char is None or
            self.char == Pixel.BLANK or
            self.fg is None or
            self.fg.a == 0
        )

    def __add__(self, other):
        if other is None:
            return self.clone()
        char = other.char if other.char is not None else self.char
        fg = other.fg if other.fg is not None else self.fg
        bg = other.bg if other.bg is not None else self.bg
        result = Pixel(char, fg=fg, bg=bg)
        return result

    def __mul__(self, other):
        if other is None:
            return self.clone()
        if type(other) == float:
            pixel = self.clone()
            pixel.set_opacity(other)
            return pixel
        if other.bg is not None and other.bg.a == 1:
            return other.clone()
        if other.is_blank():
            char = self.char
            fg = self.fg
        else:
            char = other.char
            fg = other.fg
        bg = None
        if other.bg is None:
            bg = self.bg
        elif self.bg is None or other.bg.a == 1 or self.bg.a == 0:
            bg = other.bg
        else:
            alpha = 1 - (1 - self.bg.a) * (1 - other.bg.a)
            factor = other.bg.a
            bg = self.bg.blend(other.bg, factor, alpha)
        return Pixel(char, fg, bg)

    def __str__(self):
        return f'Pixel(char=\'{self.char}\', fg={self.fg}, bg={self.bg})'

    def __repr__(self):
        return f'Pixel(char=\'{self.char}\', fg={self.fg}, bg={self.bg})'

    def __eq__(self, other):
        if other is None:
            return False
        return (
            self.char == other.char
            and self.fg == other.fg
            and self.bg == other.bg
        )

    def set_opacity(self, opacity: float):
        if self.fg is not None:
            self.fg = self.fg.with_alpha(opacity)
        if self.bg is not None:
            self.bg = self.bg.with_alpha(opacity)
