# cSpell:disable
import colorsys

from typing import Iterable

from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from textual.color import Color
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Static, Input

from utils.color import get_contrasting_color


class HuePicked(Message):

    def __init__(self, h: float | None) -> None:
        super().__init__()
        self.h = h


class ColorPicked(Message):

    def __init__(self, color: Color | None) -> None:
        super().__init__()
        self.color = color


class HueBar(Widget):

    DEFAULT_CSS = """
      HueBar {
        height: 1;
        padding: 0 1;
        color: transparent;
        background: transparent;
      }
    """

    h = reactive(None)
    cursor = reactive(0)

    def __init__(self, value: Color | None) -> None:
        super().__init__()
        self.value = value
        self.h_frac = None
        self.mouse_capturing = False

    def on_mouse_move(self, event) -> None:
        if self.mouse_capturing:
            self.handle_cursor_move(event)

    def on_mouse_up(self, event):
        self.release_mouse()
        self.mouse_capturing = False

    def on_mouse_down(self, event) -> None:
        self.capture_mouse()
        self.mouse_capturing = True
        self.handle_cursor_move(event)

    def handle_cursor_move(self, event):
        cursor = event.screen_x - self.content_region.x
        if cursor == self.cursor:
            return
        self.cursor = cursor
        h = (self.cursor) * self.h_frac
        if h < 0 or h > 1:
            return
        r, g, b = self.value.rgb
        _, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = r * 255
        g = g * 255
        b = b * 255
        self.post_message(HuePicked(h=h))

    def calculate_h_frac(self):
        self.h_frac = 1 / (self.size.width - 1)

    def calculate_cursor(self):
        if self.cursor is not None:
            return
        r, g, b = self.value.rgb
        self.cursor, _, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)

    def on_resize(self):
        self.calculate_h_frac()
        self.calculate_cursor()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        if self.h_frac is None:
            self.calculate_h_frac()
        if self.cursor is None:
            self.calculate_cursor()
        segments = []

        for i in range(self.size.width):
            h = i * self.h_frac
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            color = RichColor.from_rgb(r * 255, g * 255, b * 255)
            style = Style(bgcolor=color)
            symbol = "🮀"
            if i == self.cursor:
                symbol = " "
            segments.append(Segment(symbol, style))

        return Strip(segments)

    def render(self):
        return self


class ColorPickArea(Widget):

    DEFAULT_CSS = """
      ColorPickArea {
        color: transparent;
        background: red;
        margin: 1;
        height: 6;
      }
    """

    value = reactive(None)
    h = reactive(None)
    cursor = reactive(None)

    def __init__(self, value: Color | None, h: float | None) -> None:
        super().__init__()
        self.value = value
        self.h = h
        self.s_frac = None
        self.v_frac = None
        self.mouse_capturing = False

    def on_mouse_move(self, event) -> None:
        if self.mouse_capturing:
            self.handle_color_pick(event)

    def on_mouse_up(self, event):
        self.release_mouse()
        self.mouse_capturing = False

    def on_mouse_down(self, event) -> None:
        self.capture_mouse()
        self.mouse_capturing = True
        self.handle_color_pick(event)

    def get_color(self) -> Color:
        if self.cursor is None:
            return Color.parse("black")
        x, y = self.cursor
        h = self.h if self.h is not None else 0
        s = (x) * self.s_frac
        v = 1 - ((y) * self.v_frac)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        return Color(r, g, b)

    def handle_color_pick(self, event) -> None:
        x = event.screen_x - self.content_region.x
        y = event.screen_y - self.content_region.y
        if self.cursor is not None:
            if x == self.cursor.x and y == self.cursor.y:
                return
        s = (x) * self.s_frac
        v = 1 - ((y) * self.v_frac)
        if s < 0 or s > 1 or v < 0 or v > 1:
            return
        self.cursor = Offset(x, y)
        color = self.get_color()
        self.post_message(ColorPicked(color=color))

    def calculate_sv_frac(self):
        self.s_frac = 1 / (self.size.width - 1)
        self.v_frac = 1 / (self.size.height - 1)

    def on_resize(self):
        self.calculate_sv_frac()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        h: float
        if self.h is None:
            h = 0
        else:
            h = self.h

        if self.s_frac is None:
            self.calculate_sv_frac()
        r, g, b = self.value.rgb
        h, _, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        if self.h is not None:
            h = self.h
        segments = []
        color_cursor = get_contrasting_color(self.value)

        for j in range(self.size.height):
            v = j * self.v_frac
            for i in range(self.size.width):
                s = i * self.s_frac
                r, g, b = colorsys.hsv_to_rgb(h, s, 1 - v)
                color = RichColor.from_rgb(int(r * 255), int(g * 255), int(b * 255))
                style = Style(bgcolor=color, color=color_cursor.rich_color)
                symbol = " "
                if self.cursor is not None:
                    if i == self.cursor.x:
                        symbol = "│"
                    if j == self.cursor.y:
                        symbol = "─"
                        if i == self.cursor.x:
                            symbol = "┼"

                segments.append(Segment(symbol, style))
            segments.append(Segment.line())

        return Strip(segments[:-1])

    def render(self):
        return self


class ColorHexCode(Widget):

    value = reactive(None)

    def __init__(self, value: Color | None) -> None:
        super().__init__()
        self.value = value
        self.preview_pixel = Static("  ")
        self.preview_pixel.styles.background = value.hex

    def watch_value(self, old_value, new_value):
        if not self.is_mounted:
            return
        self.get_child_by_type(Input).value = new_value.hex[1:]
        self.preview_pixel.styles.background = new_value.hex

    def compose(self):
        yield self.preview_pixel
        yield Static(" #")
        yield Input(
            value=self.value.hex[1:],
            restrict=r"[0-9A-Fa-f]*",
            max_length=8,
            select_on_focus=False
        )


class ColorPicker(Widget):

    DEFAULT_CSS = """
     ColorPicker {
       height: auto;
     }

    """

    target = reactive(None)
    value = reactive(None)
    _value = None

    def __init__(self, target: str, value: Color | None = None) -> None:
        super().__init__()
        self.target = target
        self.value = value
        self._value = value

    def compose(self):
        yield HueBar(self.value)
        yield ColorPickArea(self.value, h=None)
        yield ColorHexCode(self.value)

    def on_color_picked(self, event):
        self._value = event.color
        self.get_child_by_type(HueBar).value = self._value
        self.get_child_by_type(ColorPickArea).value = self._value
        self.get_child_by_type(ColorHexCode).value = self._value

    def on_hue_picked(self, event):
        event.stop()
        self.get_child_by_type(HueBar).h = event.h
        colorpickarea = self.get_child_by_type(ColorPickArea)
        colorpickarea.h = event.h
        new_color = colorpickarea.get_color()
        self.get_child_by_type(ColorHexCode).value = new_color
        self.post_message(ColorPicked(new_color))

    def watch_value(self, old_value, new_value):
        if not self.is_mounted:
            return
        self.get_child_by_type(HueBar).value = new_value
        self.get_child_by_type(ColorPickArea).value = new_value
        self.get_child_by_type(ColorHexCode).value = new_value
