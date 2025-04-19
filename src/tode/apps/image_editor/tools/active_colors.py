from textual.color import Color
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static
from textual.widget import Widget


class ColorSwapped(Message):
    pass


class ColorReset(Message):
    pass


class SwapColors(Static):
    DEFAULT_CSS = """
    SwapColors {
      color: #bebebe;
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
    }
    """

    def render(self):
        return "󰀽"  # 󰀿

    def on_click(self, event):
        self.post_message(ColorReset())


class ActiveColorsPixel(Static):

    def __init__(
        self,
        text: str,
        fg: Color | None = None,
        bg: Color | None = None
    ) -> None:
        super().__init__(text)
        self.styles.color = fg
        self.styles.background = bg


class ActiveColors(Widget):

    DEFAULT_CSS = """
      ActiveColors {
        height: auto;
        width: 100%;
        color: white;
        content-align: center middle;
        align: center middle;
        Horizontal {
          height: auto;
          align: center middle;

          SwapColors:hover {
            color: #292929;
          }
        }
        Static {
          width: auto;
        }
      }
    """

    fg = reactive(None, recompose=True)
    bg = reactive(None, recompose=True)

    def __init__(self, fg: Color, bg: Color) -> None:
        super().__init__()
        self.fg = fg
        self.bg = bg

    def compose(self):
        yield Horizontal(
            ActiveColorsPixel(" 🬭🬭🬭 ", fg=self.fg),
            SwapColors()
        )
        yield Horizontal(
            ActiveColorsPixel("█", fg=self.fg),
            ActiveColorsPixel("█", fg=self.fg),
            ActiveColorsPixel("█", fg=self.fg),
            ActiveColorsPixel("🬹", fg=self.bg),
            ActiveColorsPixel("🬓", fg=self.bg),
        )
        yield Horizontal(
            ResetColors(),
            ActiveColorsPixel("🬉🬎🬎🬄", fg=self.bg)
        )

    def on_color_swapped(self):
        _tmp = self.fg
        self.fg = self.bg
        self.bg = _tmp

    def on_color_reset(self):
        pass
        # self.fg = self.initial_fg
        # self.bg = self.initial_bg
        # active_colors = self.get_child_by_type(ActiveColors)
        # active_colors.fg = self.fg
        # active_colors.bg = self.bg

"""
 🬭🬭🬭 🗘
 ███🬹🬓
 ◩🬉🬎🬎🬄
"""
