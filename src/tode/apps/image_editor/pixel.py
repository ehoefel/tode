# cSpell:disable
from dataclasses import dataclass
from typing import Iterable

from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from textual.color import Color
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


@dataclass
class PixelProperties:

    char: str | None = None
    fg: Color | str | None = None
    bg: Color | str | None = None

    def mix(self, other):
        new_values = self._as_dict()
        for key in new_values:
            if other[key] is not None:
                new_values[key] = other[key]
        return PixelProperties(**new_values)

    def clone(self):
        return PixelProperties(char=self.char, fg=self.fg, bg=self.bg)

    def is_empty(self):
        return self.char is None and self.fg is None and self.bg is None

    def _as_list(self):
        return [self.char, self.fg, self.bg]

    def _as_dict(self):
        return {
            'char': self.char,
            'fg': self.fg,
            'bg': self.bg
        }

    def __iter__(self):
        return iter(self._as_list())

    def __getitem__(self, item):
        return self._as_dict()[item]


class Pixel(Widget):

    class Click(Message):

        def __init__(self, pixel) -> None:
            super().__init__()
            self.pixel = pixel

    # class Hover(Message):

    #     def __init__(self, pixel) -> None:
    #         super().__init__()
    #         self.pixel = pixel


    EMPTY_FG = Color.parse("#999999")
    EMPTY_BG = Color.parse("#666666")

    EMPTY_PIXEL_ODD = PixelProperties("🬗", EMPTY_FG, EMPTY_BG)
    EMPTY_PIXEL_EVEN = PixelProperties("🬤", EMPTY_FG, EMPTY_BG)

    value = reactive(None)

    DEFAULT_CSS = """
      Pixel {
        width: 1;
        height: 1;
      }

    """

    def __init__(
        self,
        pos: Offset,
        value: str | None = None,
    ) -> None:
        super().__init__()
        self.pos = pos
        self.value = value

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        value = self.value
        if self.value is None:
            bit = self.pos.y % 2
            value = [Pixel.EMPTY_PIXEL_EVEN, Pixel.EMPTY_PIXEL_ODD][bit]
        attrs = dict()
        if value.fg is not None:
            attrs['color'] = value.fg.rich_color
        if value.bg is not None:
            attrs['bgcolor'] = value.bg.rich_color
        style = Style(**attrs)
        return [Segment(value.char, style)]

    def render(self):
        return self

    def is_empty(self):
        return self.value is None or self.value.is_empty()

    def apply(self, pixel_properties: PixelProperties) -> None:
        if self.value is None:
            self.value = pixel_properties
        else:
            self.value = self.value.mix(pixel_properties)

    def get_content_width(self, container, viewport) -> int:
        return 1

    def get_content_height(self, container, viewport, width):
        return 1

    def on_mouse_down(self, event):
        self.post_message(Pixel.Click(self))
