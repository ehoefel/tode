from textual.color import Color
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static
from textual.widget import Widget

from utils.color import get_contrasting_color


class ColorSwapped(Message):
    pass


class ColorReset(Message):
    pass


class SwapColors(Static):
    DEFAULT_CSS = """
    SwapColors {
      color: #bebebe;
      width: 1;
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
        margin: 1;
        width: 100%;
        height: 3;
        Horizontal {
          width: 100%;
          content-align: center middle;
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
        fg_contrast = get_contrasting_color(self.fg)
        bg_contrast = get_contrasting_color(self.bg)
        yield Horizontal(
            ActiveColorsPixel("🭽▔▔🭾", fg=fg_contrast, bg=self.fg),
            ActiveColorsPixel(" "),
            SwapColors()
        )
        yield Horizontal(
            ActiveColorsPixel("🭼▁▁🭿", fg=fg_contrast, bg=self.fg),
            ActiveColorsPixel("▔🭾", fg=bg_contrast, bg=self.bg),
        )
        yield Horizontal(
            ResetColors(),
            ActiveColorsPixel(" "),
            ActiveColorsPixel("🭼▁▁🭿", fg=bg_contrast, bg=self.bg)
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
