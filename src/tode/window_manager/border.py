from typing import Iterable

from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style
from typing_extensions import Literal

from textual.app import RenderResult
from textual.css._error_tools import friendly_list
from textual.geometry import Size
from textual.widget import Widget

from window_manager.border_style import BorderStyle

BorderPosition = Literal["top", "left", "right", "bottom"]
"""The valid positions of the border widget."""

_VALID_BORDER_POSITIONS = {"top", "left", "right", "bottom"}


class InvalidBorderPosition(Exception):
    """Exception raised for an invalid rule orientation."""


class HorizontalBorderRenderable:
    """Renders a horizontal rule."""

    def __init__(self, characters: str | tuple[str], style: Style, width: int):
        if type(characters) == str:
            characters = (characters, characters, characters)
        self.characters = characters
        self.style = style
        self.width = width

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        start = self.characters[0]
        middle = self.characters[1]
        end = self.characters[2]
        if self.width < 3:
            yield Segment(self.width * middle, self.style)
        else:
            yield Segment(start + (self.width - 2) * middle + end, self.style)


class VerticalBorderRenderable:
    """Renders a vertical rule."""

    def __init__(self, characters: str | tuple[str], style: Style, height: int):
        if type(characters) == str:
            characters = (characters, characters, characters)
        self.characters = characters
        self.style = style
        self.height = height

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        start = self.characters[0]
        middle = self.characters[1]
        end = self.characters[2]

        new_line = Segment.line()
        mid_segment = Segment(middle, self.style)
        if self.height < 3:
            return ([mid_segment, new_line] * self.height)[:-1]

        p1 = [Segment(start, self.style), new_line]
        p2 = [mid_segment, new_line] * (self.height - 2)
        p3 = [Segment(end, self.style)]
        return p1 + p2 + p3


class Border(Widget, can_focus=False):
    """A border component for a window."""

    DEFAULT_CSS = """
    Border {
        color: white;
    }

    Border.-top, Border.-bottom {
        height: 1;
        width: 1fr;
    }

    Border.-left, Border.-right {
        width: 1;
        height: 1fr;
    }
    """

    def __init__(
        self,
        position: BorderPosition,
        style: BorderStyle | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        """Initialize a border.

        Args:
            pos: The position of the border
            name: The name of the widget.
            id: The ID of the widget in the DOM.
            classes: The CSS classes of the widget.
            disabled: Whether the widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        self.border_style = style
        self.position = position
        self.expand = True
        self.add_class(f"-{position}")
        self.set_border_style(style)

    def set_border_style(self, style):
        if not style:
            style = BorderStyle()
        self.border_style = style

    def render(self) -> RenderResult:
        border_character: str
        style = self.rich_style
        border_character = self.border_style.get_chars(self.position)
        if self.position in ["left", "right"]:
            return VerticalBorderRenderable(
                border_character, style, self.content_size.height
            )
        elif self.position in ["top", "bottom"]:
            return HorizontalBorderRenderable(
                border_character, style, self.content_size.width
            )
        else:
            raise InvalidBorderPosition(
                f"Valid borer pos are {friendly_list(_VALID_BORDER_POSITIONS)}"
            )

    def get_content_width(self, container: Size, viewport: Size) -> int:
        if self.position in ["top", "bottom"]:
            return container.width
        return 1

    def get_content_height(self, container: Size, viewport: Size, width: int):
        if self.position in ["left", "right"]:
            return 1
        return container.height

    def on_mouse_down(self, event):
        self.window.resize_start(self.pos)
