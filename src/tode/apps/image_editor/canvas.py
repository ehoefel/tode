from rich.segment import Segment

from textual.color import Color
from textual.message import Message
from textual.geometry import Size, Offset, Region
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.scroll_view import ScrollView

from .pixel import Pixel


class CanvasClick(Message):

    def __init__(self, pos: Offset) -> None:
        super().__init__()
        self.pos = pos


class RenderUpdate(Message):

    def __init__(self, layer, pos: Offset) -> None:
        super().__init__()
        self.layer = layer
        self.pos = pos


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
            pixel.alpha = self.opacity

        return pixel

    def set(self, pos: Offset, pixel: Pixel) -> None:
        data = self.data
        data_y = data[pos.y]
        data_y[pos.x] = pixel
        data[pos.y] = data_y
        self.data = data
        self.post_message(RenderUpdate(self, pos))

    def apply(self, pos: Offset, pixel: Pixel) -> None:
        curr = self.get(pos)
        new_pixel = curr.blend(pixel)
        self.set(pos, new_pixel)


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

    _layers = reactive(None)

    def __init__(
        self,
        size: Size,
        layers: list
    ) -> None:
        super().__init__(id="Canvas")
        self._size = size
        self.mouse_captured = False
        self._layers = layers

    def get_pixel(self, pos: Offset):
        """ go through the layers from top to bottom, looking for the top-most
        pixel and applying the styles of the bottom layers until it reaches the
        final result """
        if self._layers is None or len(self._layers) == 0:
            return None
        pixel: Pixel = self._layers[-1].get(pos)
        if pixel is not None and pixel.alpha == 1:
            return pixel
        for layer in reversed(self._layers[:-1]):
            if not layer.visible:
                continue
            lower_layer_pixel = layer.get(pos)
            if lower_layer_pixel is None:
                continue
            if pixel is None:
                pixel = lower_layer_pixel
            else:  # blend background
                if pixel.char in [None, Pixel.BLANK]:
                    pixel.char = lower_layer_pixel.char
                    pixel.fg = lower_layer_pixel.fg
                if pixel.bg is None:
                    pixel.bg = lower_layer_pixel.bg
                elif lower_layer_pixel.bg is not None:
                    destination = lower_layer_pixel.bg
                    pixel.bg = pixel.bg.blend(destination, factor, 1)

        return pixel

    def render_line(self, y: int):
        segments = []
        style = self.get_component_rich_style()
        transparent_char = "🬤" if y % 2 == 0 else "🬗"
        transparent_segment = Segment(transparent_char, style)
        for x in range(self._size.width):
            pixel = self.get_pixel(Offset(x, y))
            if pixel is None:
                segment = transparent_segment
            else:
                if pixel.alpha != 1:
                    bgcolor = Color.from_rich_color(style.bgcolor)
                    pixel.bg = bgcolor.blend(pixel.bg, pixel.alpha, 1)
                    if pixel.is_blank():
                        pixel.char = transparent_char
                        color = Color.from_rich_color(style.color)
                        pixel.fg = color.blend(pixel.bg, pixel.alpha, 1)

                segment = Segment(pixel.char, style=pixel.style)

            segments.append(segment)

        return Strip(segments)

    def on_mouse_move(self, event):
        pass
        # if not self.mouse_captured:
        #     return
        # if (
        #     event.x < 0
        #     or event.y < 0
        #     or event.x >= len(self.data)
        #     or event.y >= len(self.data[0])
        # ):
        #     return
        # print("mouse_move", event.x, event.y)
        # event.stop()
        # pixel = self.data[event.y][event.x]
        # self.post_message(CanvasClick(pixel=pixel))

    def on_mouse_down(self, event):
        print("mouse_down", event)
        pos = Offset(x=event.x, y=event.y)
        self.post_message(CanvasClick(pos=pos))

    def on_mouse_up(self, event):
        print("mouse_up")
        # self.release_mouse()
        # self.mouse_captured = False

    def on_render_update(self, message: RenderUpdate) -> None:
        layer = message.layer
        pos = message.pos
        if pos is None:
            self.refresh()
        else:
            self.refresh_line(pos.y)

    def get_content_width(self, container, viewport) -> int:
        return self._size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self._size.height

    def watch__layers(self, old_value, new_value) -> None:
        if new_value is None:
            return
        for layer in new_value:
            layer.post_message = self.post_message
