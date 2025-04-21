# cSpell:disable
import math
from typing import NamedTuple

from rich.segment import Segment

from textual.message import Message
from textual.geometry import Size, Offset
from textual.reactive import reactive, var
from textual.scroll_view import ScrollView
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Input

from utils.unicode import Unicode


class BrushSelected(Message):

    def __init__(self, brush: str | None) -> None:
        super().__init__()
        self.brush = brush


class BrushOptions(ScrollView):

    COMPONENT_CLASSES = (
        "-option-hover",
        "-option-selected"
    )

    DEFAULT_CSS = """

     .-option-hover {
       background: black 20%;
     }

     .-option-selected {
       text-style: reverse;
     }

     BrushOptions {
       width: 100%;
       height: 100%;
       scrollbar-size: 1 1;
       scrollbar-gutter: stable;
       background: white;
       color: black;

     }

    """

    filter = reactive(None)
    virtual_size = reactive(None)
    cursor = reactive(None)
    selected_brush = reactive(None)
    brush_options = reactive(None)

    def __init__(self, brush_options: list, selected_brush) -> None:
        super().__init__()
        self.filter = filter
        self.brush_options = brush_options
        self.brush_area = []
        self.selected_brush = selected_brush
        self.virtual_size = Size(width=20, height=20)

    def get_content_width(self, container, viewport) -> int:
        return container.width - 1  # - 1 for the scrollbar

    def get_content_height(self, container, viewport, width: int) -> int:
        return container.height - 0  # - 2 because of filter and bottom line

    def on_resize(self) -> None:
        width = self.size.width - 1  # - 1 for the scrollbar
        if self.brush_options is None:
            return
        height = math.ceil(len(self.brush_options) / width)
        self.virtual_size = Size(width=width, height=height)

    def on_mouse_move(self, event) -> None:
        x = event.screen_x - self.content_region.x
        y = event.screen_y - self.content_region.y
        if self.cursor is not None:
            if x == self.cursor.x and y == self.cursor.y:
                return
        self.cursor = Offset(x, y)
        if not self.mouse_hover:
            self.cursor = None

    def on_leave(self, event) -> None:
        if not self.mouse_hover:
            self.cursor = None

    def on_enter(self, event) -> None:
        if not self.mouse_hover:
            self.cursor = None

    def on_click(self, event) -> None:
        x = event.x
        y = event.y + self.scroll_offset.y
        if y >= len(self.brush_area):
            return
        if x >= len(self.brush_area[y]):
            return
        char = self.brush_area[y][x]
        self.selected_brush = char
        self.post_message(BrushSelected(char))

    def watch_brush_options(self, old_value, new_value) -> None:
        self.build_brush_area()
        self.on_resize()

    def watch_virtual_size(self, old_value, new_value) -> None:
        self.build_brush_area()

    def build_brush_area(self):
        if self.brush_options is None:
            return
        if self.size is None or self.size.width <= 1:
            return
        line_length = self.size.width - 1
        nr_lines = math.ceil(len(self.brush_options) / line_length)
        self.brush_area = []
        for n in range(nr_lines):
            curr_idx = n * line_length
            next_idx = curr_idx + line_length
            line_chars = self.brush_options[curr_idx:next_idx]
            self.brush_area.append(line_chars)

    def render_line(self, y: int) -> Strip:
        if y >= len(self.brush_area):
            return Strip([])
        scroll_x, scroll_y = self.scroll_offset  # The current scroll position
        content_y = y + scroll_y
        if content_y > len(self.brush_area):
            return Strip([])
        line_chars = "".join(self.brush_area[content_y])

        style = self.get_component_rich_style()
        segments = []
        render_cursor = (
            self.cursor is not None
            and y == self.cursor.y
            and self.cursor.x < len(line_chars)
        )
        render_selected = (
            self.selected_brush is not None
            and self.selected_brush in line_chars
        )
        render_either = render_cursor or render_selected
        render_both = render_cursor and render_selected
        render_one = (
            (render_both and line_chars[self.cursor.x] == self.selected_brush)
            or (not render_both and render_either)
        )

        if render_selected:
            style_selected = self.get_component_rich_style("-option-selected")
        if render_cursor:
            style_hover = self.get_component_rich_style("-option-hover")

        if render_one:
            if render_selected:
                special_style = style_selected
                x = line_chars.index(self.selected_brush)
            else:
                special_style = style_hover
                x = self.cursor.x
            segments.append(Segment(line_chars[0:x], style))
            segments.append(Segment(line_chars[x], special_style))
            segments.append(Segment(line_chars[x + 1:], style))
        elif render_both:
            x1 = line_chars.index(self.selected_brush)
            x2 = self.cursor.x
            s1 = style_selected
            s2 = style_hover
            if x1 > x2:
                x1, x2 = (x2, x1)
                s1, s2 = (s2, s1)
            segments.append(Segment(line_chars[0:x1], style))
            segments.append(Segment(line_chars[x1], s1))
            segments.append(Segment(line_chars[x1 + 1: x2], style))
            segments.append(Segment(line_chars[x2], s2))
            segments.append(Segment(line_chars[x2 + 1:], style))
        else:
            segments.append(Segment(line_chars, style=style))

        return Strip(segments)


class BrushSelector(Widget):

    DEFAULT_CSS = """
      BrushSelector {
         layout: vertical;
         height: 10;
         padding: 0 1;
         Input, Input:hover, Input:focus {
           height: 1;
           width: 100%;
           border: none;
           text-align: left;
           padding: 0;

           .input--placeholder {
             text-style: italic;
           }
         }
      }

    """

    value = reactive(None)
    brush_unicodes = var([])
    filter_text = var("")

    def __init__(self, value: str | None = None) -> None:
        super().__init__()
        self.value = value
        brush_unicodes = []
        enabled_blocks = [
            'Basic Latin',
            'Latin-1 Supplement',
            'Box Drawing',
            'Block Elements',
            'Symbols for Legacy Computing'
        ]

        for block in enabled_blocks:
            brush_unicodes += Unicode.get_block_chars(block)

        self.brush_unicodes = brush_unicodes

        self.input = Input(placeholder=" filter", select_on_focus=False)
        self.brush_options = BrushOptions(brush_options=self.brush_unicodes,
                                          selected_brush=self.value)

    def watch_brush_unicodes(self, old_value, new_value) -> None:
        self.build_filtered_brush_unicodes()

    def build_filtered_brush_unicodes(self):
        def filter(char):
            if char.lower() == self.filter_text.lower():
                return True
            if self.filter_text.lower() in char.name().lower():
                return True
            return False

        filtered = [char for char in self.brush_unicodes if filter(char)]
        self.filtered_brush_unicodes = filtered
        if hasattr(self, "brush_options"):
            self.brush_options.brush_options = self.filtered_brush_unicodes

    def watch_filter_text(self, old_value, new_value):
        self.build_filtered_brush_unicodes()

    def on_input_changed(self, event):
        self.filter_text = event.value

    def on_brush_selected(self, event):
        self.value = event.brush

    def compose(self):
        yield self.input
        yield self.brush_options
