from textual.containers import Grid
from textual.geometry import Size
from textual.widget import Widget


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

    def __init__(self, tools: dict):
        super().__init__()
        self.tools = tools

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
        yield self.tools['active_colors']

    def get_content_width(self, container, viewport) -> int:
        return 15

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height
