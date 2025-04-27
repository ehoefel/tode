# cSpell:disable
from typing import Iterable

from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from textual.color import Color
from textual.message import Message
from textual.reactive import reactive, var
from textual.widgets import Static
from textual.widget import Widget

from ..utils.color import get_contrasting_color


class ColorSwapped(Message):
    pass


class ColorReset(Message):
    pass


class SwapColors(Static):
    DEFAULT_CSS = """
    SwapColors {
      color: #bebebe;
      width: 1;

      &:hover {
          color: #292929;
      }
    }
    """

    def render(self):
        return "🗘 "

    def on_click(self, event):
        self.post_message(ColorSwapped())


class ResetColors(Static):
    DEFAULT_CSS = """
    ResetColors {
      color: black;
      width: 1;
    }
    """

    def render(self):
        return "󰀽"  # 󰀿

    def on_click(self, event):
        self.post_message(ColorReset())


class ActiveColors(Widget):

    DEFAULT_CSS = """
      ActiveColors {
        margin: 1;
        width: 100%;
        content-align: center middle;
        height: auto;
      }
    """

    fg = reactive(None)
    bg = reactive(None)

    def __init__(self, fg: Color, bg: Color) -> None:
        super().__init__()
        self.fg = fg
        self.bg = bg

    def render(self):
        return self

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        fg_contrast = get_contrasting_color(self.fg)
        bg_contrast = get_contrasting_color(self.bg)

        sfg = Style(color=fg_contrast.rich_color, bgcolor=self.fg.rich_color)
        sbg = Style(color=bg_contrast.rich_color, bgcolor=self.bg.rich_color)

        segments = []
        segments.append(Segment("🭽▔▔🭾", style=sfg))
        segments.append(Segment("  "))
        segments.append(Segment.line())
        segments.append(Segment("🭼▁▁🭿", style=sfg))
        segments.append(Segment("▔🭾", style=sbg))
        segments.append(Segment.line())
        segments.append(Segment("  "))
        segments.append(Segment("🭼▁▁🭿", style=sbg))
        return segments

    def get_content_width(self, container, viewport) -> int:
        return 6

    def get_content_height(self, container, viewport, width: int) -> int:
        return 3


class ColorArea(Widget):

    DEFAULT_CSS = """
      ColorArea {
        layers: colors buttons;
        width: 100%;
        height: auto;
        align: center middle;
        content-align: center middle;
        ActiveColors {
          layer: colors;
        }
        SwapColors {
          layer: buttons;
          offset: 3 1;
        }
        ResetColors {
          layer: buttons;
          offset: -2 2;
        }
      }

    """

    fg = var(None)
    bg = var(None)

    def __init__(self, fg: Color, bg: Color) -> None:
        super().__init__()
        self.active_colors = ActiveColors(fg, bg)
        self.swap_colors = SwapColors()
        self.reset_colors = ResetColors()
        self.fg = fg
        self.bg = bg

    def watch_fg(self, old_value, new_value):
        self.active_colors.fg = new_value

    def watch_bg(self, old_value, new_value):
        self.active_colors.bg = new_value

    def on_color_swapped(self):
        self.fg, self.bg = self.bg, self.fg

    def compose(self):
        yield self.active_colors
        yield self.swap_colors
        yield self.reset_colors
