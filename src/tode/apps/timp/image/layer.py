from textual.color import Color
from textual.geometry import Size, Offset, Region
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget

from .pixel import Pixel


class LayerUpdate(Message):

    def __init__(
        self,
        layer,
        offsets: list[Offset] | None = None,
        lines: list[int] | None = None
    ) -> None:
        super().__init__()
        self.layer = layer
        self._offsets = offsets
        self._lines = lines

    @property
    def region(self):
        if self._offsets is not None:
            min_x = None
            min_y = None
            max_x = None
            max_y = None
            for offset in self._offsets:
                if min_x is None or offset.x < min_x:
                    min_x = offset.x
                if max_x is None or offset.x > max_x:
                    max_x = offset.x
                if min_y is None or offset.y < min_y:
                    min_y = offset.y
                if max_y is None or offset.y > max_y:
                    max_y = offset.y
            return Region.from_corners(min_x, min_y, max_x + 1, max_y + 1)

    @property
    def offsets(self):
        return self._offsets if self._offsets is not None else []

    @property
    def lines(self):
        return self._lines if self._lines is not None else []


class Layer(Widget):

    active: var[bool] = var(False)
    visible: var[bool] = var(False)
    linked: var[bool] = var(False)

    def __init__(
        self,
        name: str,
        size: Size,
        data: list | None = None,
        visible: bool | None = True,
        linked: bool | None = True,
        active: bool | None = False,
        opacity: float | None = 1.0
    ) -> None:
        super().__init__(name=name)
        if data is None:
            data = [[None] * size.width for i in range(size.height)]
        self.data = data
        self._region = Region.from_offset(Offset(0, 0), size)
        self.visible = visible
        self.active = active
        self.linked = linked
        self._opacity = opacity

    def __str__(self):
        return f'Layer(name={self.name})'

    def __repr__(self):
        return f'Layer(name={self.name})'

    def fill_with(name, size, color: Color):
        data = [
            [Pixel(Pixel.BLANK, bg=color) for j in range(size.width)]
            for i in range(size.height)
        ]
        return Layer(name, size, data)

    def get(self, pos: Offset) -> Pixel | None:
        if not self._region.contains_point(pos):
            return None
        pixel = self.data[pos.y][pos.x]
        if pixel is not None:
            pixel = pixel.clone()
            pixel.set_opacity(self._opacity)

        return pixel

    def get_line(self, y: int) -> list[Pixel | None] | None:
        if self.data[y] is None:
            return self.data[y]
        line = []
        for x in range(self._region.width):
            pixel = self.data[y][x]
            if pixel is not None:
                pixel = pixel * self._opacity
            line.append(pixel)
        return line

    def set(self, pos: Offset, pixel: Pixel) -> None:
        self.data[pos.y][pos.x] = pixel
        self.post_message(LayerUpdate(self, offsets=[pos]))

    def apply(self, pos: Offset, pixel: Pixel) -> None:
        self.set(pos, self.data[pos.y][pos.x] + pixel)
