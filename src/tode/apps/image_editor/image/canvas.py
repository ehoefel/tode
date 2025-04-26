# cSpell: disable
from __future__ import annotations

from textual.color import Color
from textual.message import Message
from textual.geometry import Size, Offset, Region
from textual.reactive import reactive
from textual.strip import Strip
from textual.scroll_view import ScrollView

from .pixel import Pixel


class CanvasClick(Message):

    def __init__(self, pos: Offset) -> None:
        super().__init__()
        self.pos = pos


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


def pixel_compute(p1: Pixel | None, p2: Pixel | None) -> Pixel | None:
    if p1 is None:
        return p2
    return p1 * p2


class LayerView:

    def __init__(
        self,
        size: Size,
        base: LayerView | None,
        layer: Layer
    ) -> None:
        self.size = size
        self.base = base
        self.layer = layer
        self._render_cache = [None] * size.height
        self._result = [None] * size.height
        self.dirty_lines = [y for y in self.size.line_range]
        self.dirty_pixels = []

    def is_dirty(self, y: int):
        if y in self.dirty_lines:
            return True
        for pos in self.dirty_pixels:
            if pos.y == y:
                return True
        return False

    def clear_dirty(self, y: int):
        if y in self.dirty_lines:
            self.dirty_lines.remove(y)
        pixels = [p for p in self.dirty_pixels if p.y == y]
        for p in pixels:
            self.dirty_pixels.remove(p)

    def __str__(self):
        return f'LayerView(layer={self.layer.name})'

    def __repr__(self):
        return f'LayerView(layer={self.layer.name})'

    def _get_uncached(self, pos: Offset) -> None:
        layer_pixel = self.layer.get(pos)
        if self.base is None:
            return layer_pixel

        base_pixel = self.base.get(pos)
        return pixel_compute(base_pixel, layer_pixel)

    def get(self, pos: Offset) -> Pixel:
        y, x = pos
        line = self._result[y]
        if y in self.dirty_lines:
            line = self._get_line_uncached(y)
            self._result[y] = line
            self.dirty_lines.remove(y)
        pixel = line[x]
        if pos in self.dirty_pixels:
            pixel = self._get_uncached(pos)
            self._result[y][x] = pixel
            self.dirty_pixels.remove(pos)

        return pixel

    def _get_line_uncached(self, y: int) -> list[Pixel]:
        layer_line = self.layer.get_line(y)
        if self.base is None:
            return layer_line

        base_line = self.base.get_line(y)
        if layer_line is None:
            return base_line

        w = self.size.width
        return [pixel_compute(base_line[x], layer_line[x]) for x in range(w)]

    def get_line(self, y: int) -> list[Pixel]:
        if self.is_dirty(y):
            self._result[y] = self._get_line_uncached(y)
            self.clear_dirty(y)
        return self._result[y]

    def _cache_render_line(self, y: int) -> Strip:
        data_row = self.get_line(y)
        line = [pixel.segment for pixel in data_row]
        self._render_cache[y] = Strip(line).simplify()
        self.clear_dirty(y)

    def render_line(self, y: int) -> Strip:
        if self.is_dirty(y):
            self._cache_render_line(y)
        return self._render_cache[y]

    def update(self, update: LayerUpdate) -> None:
        for pos in update.offsets:
            self.dirty_pixels.append(pos)
        for line in update.lines:
            self.dirty_lines.append(line)


class Layer:

    def __init__(
        self,
        name: str,
        size: Size,
        data: list | None = None,
        visible: bool | None = True,
        opacity: float | None = 1.0
    ) -> None:
        self.name = name
        if data is None:
            data = [[None] * size.width for i in range(size.height)]
        self.data = data
        self.region = Region.from_offset(Offset(0, 0), size)
        self.visible = visible
        self.opacity = opacity

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
        if not self.region.contains_point(pos):
            return None
        pixel = self.data[pos.y][pos.x]
        if pixel is not None:
            pixel = pixel.clone()
            pixel.set_opacity(self.opacity)

        return pixel

    def get_line(self, y: int) -> list[Pixel | None] | None:
        if self.data[y] is None:
            return self.data[y]
        line = []
        for x in range(self.region.width):
            pixel = self.data[y][x]
            if pixel is not None:
                pixel = pixel * self.opacity
            line.append(pixel)
        return line

    def set(self, pos: Offset, pixel: Pixel) -> None:
        self.data[pos.y][pos.x] = pixel
        self.post_message(LayerUpdate(self, offsets=[pos]))

    def apply(self, pos: Offset, pixel: Pixel) -> None:
        self.set(pos, self.data[pos.y][pos.x] + pixel)


class Canvas(ScrollView):

    DEFAULT_CSS = """
      Canvas {
        width: auto;
        height: auto;
        color: #666666;
        background: #9E9E9E;
        overflow: hidden hidden;
      }
    """

    view: reactive[LayerView] = reactive(None)

    def __init__(
        self,
        size: Size,
        view: LayerView | None = None
    ) -> None:
        super().__init__(id="Canvas", name="Canvas")
        self._size = size
        self.mouse_captured = False
        self.view = view

    def __str__(self):
        return 'Canvas()'

    def __repr__(self):
        return 'Canvas()'

    def render_line(self, y: int):
        return self.view.render_line(y)

    def on_mouse_move(self, event):
        if not self.mouse_captured:
            return
        pos = Offset(x=event.x, y=event.y)
        if not self._size.contains_point(pos):
            return
        event.stop()
        self.post_message(CanvasClick(pos))

    def on_mouse_down(self, event):
        pos = Offset(x=event.x, y=event.y)
        self.post_message(CanvasClick(pos=pos))
        self.mouse_captured = True
        self.capture_mouse()

    def on_mouse_up(self, event):
        self.release_mouse()
        self.mouse_captured = False

    def get_content_width(self, container, viewport) -> int:
        return self._size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self._size.height

    def get_line(self, y: int) -> list[Pixel]:
        chars = ["🬤", "🬗"]
        style = self.get_component_rich_style()
        fg = Color.from_rich_color(style.color)
        bg = Color.from_rich_color(style.bgcolor)
        return [Pixel(chars[y % 2], fg, bg)] * self._size.width
