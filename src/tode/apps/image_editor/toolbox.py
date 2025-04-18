from textual.color import Color
from textual.containers import Grid, Horizontal
from textual.geometry import Size
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static


class ColorSwapped(Message):
    pass


class ColorReset(Message):
    pass


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
            if fg:
                self.styles.color = fg
            if bg:
                self.styles.background = bg

    def __init__(
        self,
        fg: Color,
        bg: Color
    ) -> None:
        super().__init__()
        self.fg = fg
        self.bg = bg

    def compose(self):
        yield Horizontal(
            ActiveColors.ActiveColorsPixel(" 🬭🬭🬭 ", fg=self.fg),
            ActiveColors.SwapColors()
        )
        yield Horizontal(
            ActiveColors.ActiveColorsPixel("█", fg=self.fg),
            ActiveColors.ActiveColorsPixel("█", fg=self.fg),
            ActiveColors.ActiveColorsPixel("█", fg=self.fg),
            ActiveColors.ActiveColorsPixel("🬹", fg=self.bg),
            ActiveColors.ActiveColorsPixel("🬓", fg=self.bg),
        )
        yield Horizontal(
            ActiveColors.ResetColors(),
            ActiveColors.ActiveColorsPixel("🬉🬎🬎🬄", fg=self.bg)
        )

"""
 🬭🬭🬭 🗘
 ███🬹🬓
 ◩🬉🬎🬎🬄
"""


class Tool(Widget):

    symbol: str

    def render(self):
        return self.symbol

    def get_content_width(self, container, viewport) -> int:
        return 1

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return 1


class MoveTool(Tool):
    symbol = ""


class RectangleSelect(Tool):
    symbol = "󰒆"


class FreeSelect(Tool):
    symbol = "󱇺"


class FuzzySelect(Tool):
    symbol = "󰁨"


class Crop(Tool):
    symbol = "󰆞"


class Rotate(Tool):
    symbol = "󰑨"


class WarpTransform(Tool):
    symbol = "󱪁"


class BucketFill(Tool):
    symbol = ""


class Pencil(Tool):
    symbol = ""


class Eraser(Tool):
    symbol = "󰇾"


class Clone(Tool):
    symbol = "󰴹"


class Smudge(Tool):
    symbol = "󰆽"


class Paths(Tool):
    symbol = ""


class Text(Tool):
    symbol = "󰚞"


class ColorPicker(Tool):
    symbol = "󰈋"


class Zoom(Tool):
    symbol = "󰍉"


class Toolbox(Widget):

    DEFAULT_CSS = """
      Toolbox {
        dock: left;
        layout: vertical;
        width: auto;
        height: 100%;
        background: #434343;
        padding-top: 3;
        & > Grid {
          width: 100%;
          height: auto;
          grid-size: 5;
          grid-gutter: 0;
          grid-columns: auto;
          & > Tool {
            margin: 0;
            color: #bebebe;
            height: auto;
            width: auto;
            padding: 0 1;
          }
        }
      }
    """

    initial_fg = Color.parse("black")
    initial_bg = Color.parse("white")

    def __init__(self):
        super().__init__()
        self.fg = self.initial_fg
        self.bg = self.initial_bg

    def compose(self):
        yield Grid(
            MoveTool(),
            RectangleSelect(),
            FreeSelect(),
            FuzzySelect(),
            Crop(),
            Rotate(),
            WarpTransform(),
            BucketFill(),
            Pencil(),
            Eraser(),
            Clone(),
            Smudge(),
            Paths(),
            Text(),
            ColorPicker(),
            Zoom()
        )
        yield ActiveColors(fg=self.fg, bg=self.bg)

    def get_content_width(self, container, viewport) -> int:
        return 15

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height

    def on_color_swapped(self):
        _tmp = self.fg
        self.fg = self.bg
        self.bg = _tmp
        active_colors = self.get_child_by_type(ActiveColors)
        active_colors.fg = self.fg
        active_colors.bg = self.bg

    def on_color_reset(self):
        self.fg = self.initial_fg
        self.bg = self.initial_bg
        active_colors = self.get_child_by_type(ActiveColors)
        active_colors.fg = self.fg
        active_colors.bg = self.bg
