from typing import NamedTuple
from typing_extensions import Literal

BorderStyleAttributes = Literal[
    "top",
    "left",
    "right",
    "bottom",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right"
]


class BorderStyle(NamedTuple):
    """A border character style definition"""

    top: str = "-"
    left: str = "|"
    right: str = "|"
    bottom: str = "-"
    top_left: str = "/"
    top_right: str = "\\"
    bottom_left: str = "\\"
    bottom_right: str = "/"

    def get_chars(self, position):
        if position == "top":
            return (self.top_left, self.top, self.top_right)
        if position == "left":
            return (self.top_left, self.left, self.bottom_left)
        if position == "right":
            return (self.top_right, self.right, self.bottom_right)
        if position == "bottom":
            return (self.bottom_left, self.bottom, self.bottom_right)
