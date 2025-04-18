# cSpell:disable
from rich.segment import Segment
from rich.style import Style

from textual.geometry import Offset


class Pixel():

    EMPTY_PIXEL_ODD = "🬗"
    EMPTY_PIXEL_EVEN = "🬤"
    EMPTY_STYLE = Style(color="grey39", bgcolor="grey62")

    def __init__(
        self,
        pos: Offset,
        value: str | None = None
    ) -> None:
        self.pos = pos
        self.value = value

    def is_empty(self):
        return self.value is None

    @property
    def segment(self):
        if self.is_empty():
            bit = self.pos.y % 2
            text = [Pixel.EMPTY_PIXEL_EVEN, Pixel.EMPTY_PIXEL_ODD][bit]
            return Segment(text, Pixel.EMPTY_STYLE)
        return Segment(self.value)
