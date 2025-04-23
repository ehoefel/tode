# cSpell:disable

from rich.style import Style

from textual.color import Color


class Pixel:

    BLANK = " "

    def __init__(
        self,
        char: str,
        fg: Color | None = None,
        bg: Color | None = None,
        alpha: float | None = None
    ) -> None:
        super().__init__()
        self.char = char
        self.fg = fg
        self.bg = bg
        self.alpha = alpha

    @property
    def style(self) -> Style:
        kwargs = dict()
        if self.fg is not None:
            fg = self.fg
            if self.alpha is not None:
                fg = fg.with_alpha(self.alpha)
            kwargs['color'] = fg.rich_color
        if self.bg is not None:
            bg = self.bg
            if self.alpha is not None:
                bg = bg.with_alpha(self.alpha)
            kwargs['bgcolor'] = bg.rich_color
        return Style(**kwargs)

    def clone(self):
        return Pixel(self.char, self.fg, self.bg)

    def is_blank(self):
        return self.char == Pixel.BLANK
