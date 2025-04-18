from typing import Iterable

from rich.console import Console, ConsoleOptions
from rich.segment import Segment

from textual.geometry import Size, Offset
from textual.strip import Strip
from textual.widget import Widget

from apps.image_editor.pixel import Pixel


class Canvas(Widget):

    DEFAULT_CSS = """
      Canvas {
        width: auto;
        height: auto;
      }
    """

    canvas_size: Size
    data: list

    def __init__(
        self,
        size: Size,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.canvas_size = size
        self.data = []
        for i in range(size.height):
            row = []
            for j in range(size.width):
                row.append(Pixel(Offset(x=j, y=i)))
            self.data.append(row)

    def render(self):
        return self

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        data = []
        for row in self.data:
            data += [pixel.segment for pixel in row] + [Segment.line()]
        return Strip(data[:-1])

    def get_content_width(self, container, viewport) -> int:
        return self.canvas_size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self.canvas_size.height
