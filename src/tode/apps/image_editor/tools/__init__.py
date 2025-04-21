
from .tool import Tool
from .pencil import Pencil


class MoveTool(Tool):
    symbol = ""


class RectangleSelect(Tool):
    symbol = "󰒆"


class FreeSelect(Tool):
    symbol = "󰴲"


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


class Eraser(Tool):
    symbol = "󰇾"


class Clone(Tool):
    symbol = "󰴹"


class Smudge(Tool):
    symbol = "󰆽"


class Paths(Tool):
    symbol = "󰕙"


class Text(Tool):
    symbol = "󰚞"


class ColorPicker(Tool):
    symbol = "󰈋"


class Zoom(Tool):
    symbol = "󰍉"


tool_list = [
    MoveTool,
    RectangleSelect,
    FreeSelect,
    FuzzySelect,
    Crop,
    Rotate,
    WarpTransform,
    BucketFill,
    Pencil,
    Eraser,
    Clone,
    Smudge,
    Paths,
    Text,
    ColorPicker,
    Zoom
]
