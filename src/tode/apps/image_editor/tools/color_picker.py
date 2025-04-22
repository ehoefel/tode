# cSpell:disable
import colorsys

from typing import Iterable, NamedTuple

from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from textual.color import Color
from textual.geometry import Offset
from textual.message import Message
from textual.reactive import reactive, var
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Static, Input

from utils.color import get_contrasting_color


class HSV(NamedTuple):
    h: float | None
    s: float | None
    v: float | None

    def to_color(self):
        h, s, v = self
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        return Color(r, g, b)

    def from_color(color: Color):
        if color is None:
            return HSV(None, None, None)
        r, g, b = color.rgb
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        return HSV(h, s, v)


class HuePicked(Message):

    def __init__(self, h: float) -> None:
        super().__init__()
        self.h = h


class SvPicked(Message):

    def __init__(self, sv: tuple) -> None:
        super().__init__()
        self.sv = sv


class ColorPicked(Message):

    def __init__(self, color: Color) -> None:
        super().__init__()
        self.color = color


class ColorHexPicked(Message):

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


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

    def __init__(self, h: float | None) -> None:
        super().__init__()
        self.h = h
        self.h_frac = None
        self.mouse_capturing = False

    def on_click(self, event) -> None:
        event.stop()

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
        h = (cursor) * self.h_frac
        if h < 0 or h > 1:
            return
        self.h = h
        self.post_message(HuePicked(h=h))

    def calculate_h_frac(self):
        self.h_frac = 1 / (self.size.width - 1)

    def calculate_cursor(self):
        return round(self.h / self.h_frac)

    def on_resize(self):
        self.calculate_h_frac()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        if self.h_frac is None:
            self.calculate_h_frac()
        cursor = self.calculate_cursor()
        segments = []

        for i in range(self.size.width):
            h = i * self.h_frac
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            color = RichColor.from_rgb(r * 255, g * 255, b * 255)
            style = Style(bgcolor=color)
            symbol = "🮀"
            if i == cursor:
                symbol = " "
            segments.append(Segment(symbol, style))

        return Strip(segments)

    def render(self):
        return self


class SVPickArea(Widget):

    DEFAULT_CSS = """
      SVPickArea {
        color: transparent;
        background: red;
        margin: 1;
        height: 6;
      }
    """

    h = reactive(None)
    s = reactive(None)
    v = reactive(None)

    def __init__(self, h: float | None, sv: tuple | None) -> None:
        super().__init__()
        self.h = h
        if sv is not None:
            self.s, self.v = sv
        self.s_frac = None
        self.v_frac = None
        self.mouse_capturing = False

    def on_click(self, event) -> None:
        event.stop()

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

    def get_color(self, cursor: Offset) -> Color:
        h = self.h
        x, y = cursor
        s = x * self.s_frac
        v = 1 - (y * self.v_frac)
        hsv = HSV(h, s, v)
        return hsv.to_color()

    def handle_color_pick(self, event) -> None:
        x = event.screen_x - self.content_region.x
        y = event.screen_y - self.content_region.y
        s = x * self.s_frac
        v = 1 - (y * self.v_frac)
        if s < 0 or s > 1 or v < 0 or v > 1:
            """ Mouse most likely outside of the color area """
            return
        self.s = s
        self.v = v
        self.post_message(SvPicked(sv=(s, v)))

    def calculate_sv_frac(self):
        self.s_frac = 1 / (self.size.width - 1)
        self.v_frac = 1 / (self.size.height - 1)

    def on_resize(self):
        self.calculate_sv_frac()

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        if self.s_frac is None:
            self.calculate_sv_frac()

        segments = []
        cursor_x = round(self.s / self.s_frac)
        cursor_y = round((1 - self.v) / self.v_frac)
        cursor_pos = Offset(cursor_x, cursor_y)
        color_under_cursor = self.get_color(cursor_pos)
        color_cursor = get_contrasting_color(color_under_cursor)

        for j in range(self.size.height):
            vj = 1 - (j * self.v_frac)  # we want the color value to go 1 -> 0
            for i in range(self.size.width):
                si = i * self.s_frac
                hsv = HSV(h=self.h, s=si, v=vj)
                color = hsv.to_color().rich_color
                style = Style(bgcolor=color, color=color_cursor.rich_color)
                if j == cursor_pos.y and i == cursor_pos.x:
                    symbol = "┼"
                elif j == cursor_pos.y:
                    symbol = "─"
                elif i == cursor_pos.x:
                    symbol = "│"
                else:
                    symbol = " "

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
        if value is not None:
            self.preview_pixel.styles.background = value.hex

    def hex_to_color(self, hex_value):
        return Color.parse(f'#{hex_value}')

    def watch_value(self, old_value, new_value):
        if not self.is_mounted:
            return
        input = self.get_child_by_type(Input)
        input_color = self.hex_to_color(input.value)
        if input_color != new_value:
            with input.prevent(Input.Changed):
                input.value = new_value.hex[1:]
        self.preview_pixel.styles.background = new_value.hex

    def on_input_changed(self, message):
        message.stop()
        if len(message.value) not in [3, 4, 6, 8]:
            return
        if message.value == self.value.hex[1:]:
            return
        self.post_message(ColorHexPicked(message.value))

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

    value = var(None)

    def __init__(self, value: Color | None = None) -> None:
        super().__init__()
        if value is None:
            value = Color.parse("black")
        hsv = HSV.from_color(value)
        h, s, v = hsv
        self.hue_bar = HueBar(h=h)
        self.color_pick_area = SVPickArea(h=h, sv=(s, v))
        self.color_hex_code = ColorHexCode(self.value)
        self.value = value

    def compose(self):
        yield self.hue_bar
        yield self.color_pick_area
        yield self.color_hex_code

    def watch_value(self, old_value, new_value):
        if old_value == new_value:
            return
        hsv = HSV.from_color(new_value)
        h, s, v = hsv
        with self.hue_bar.prevent(HuePicked):
            self.hue_bar.h = h
        with self.color_pick_area.prevent(SvPicked):
            self.color_pick_area.h = h
            self.color_pick_area.s = s
            self.color_pick_area.v = v
        with self.color_hex_code.prevent(ColorPicked):
            self.color_hex_code.value = new_value

    def on_hue_picked(self, message):
        message.stop()
        h = message.h
        s = self.color_pick_area.s
        v = self.color_pick_area.v
        self.color_pick_area.h = h
        value = HSV(h, s, v).to_color()
        with self.color_hex_code.prevent(ColorPicked):
            self.color_hex_code.value = value
        self.post_message(ColorPicked(value))

    def on_sv_picked(self, message):
        message.stop()
        s, v = message.sv
        h = self.hue_bar.h
        value = HSV(h, s, v).to_color()
        with self.color_hex_code.prevent(ColorPicked):
            self.color_hex_code.value = value
        self.post_message(ColorPicked(value))

    def on_color_hex_picked(self, message):
        color = Color.parse(f'#{message.value}')
        self.value = color
        self.post_message(ColorPicked(color))
