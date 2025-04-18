from textual.color import Color
from textual.containers import Grid, Horizontal
from textual.geometry import Size
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Placeholder, Static


class ColorSwapped(Message):
    pass


class ColorReset(Message):
    pass


class ActiveColors(Widget):

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
          color: white;
        }
        """

        def render(self):
            return "◩"

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
            ActiveColors.ActiveColorsPixel("🬕", fg=self.fg, bg=self.bg),
            ActiveColors.ActiveColorsPixel("🬂", fg=self.fg, bg=self.bg),
            ActiveColors.ActiveColorsPixel("🬹", fg=self.bg),
            ActiveColors.ActiveColorsPixel("🬓", fg=self.bg),
        )
        yield Horizontal(
            ActiveColors.ResetColors(),
            ActiveColors.ActiveColorsPixel("🬉🬎🬎🬄", fg=self.bg)
        )

"""
 🬭🬭🬭 🗘
 █🬕🬂🬹🬓
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
      layer: above;
      dock: left;
      height: 1fr;
      width: auto;
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

    def __init__(self):
        super().__init__()
        self.fg = Color.parse("white")
        self.bg = Color.parse("black")

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
        self.fg = Color.parse("white")
        self.bg = Color.parse("black")
        active_colors = self.get_child_by_type(ActiveColors)
        active_colors.fg = self.fg
        active_colors.bg = self.bg
