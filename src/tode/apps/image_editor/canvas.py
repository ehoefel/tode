from textual.containers import Horizontal
from textual.message import Message
from textual.geometry import Size, Offset
from textual.widget import Widget

from .pixel import Pixel


class CanvasClick(Message):

    def __init__(self, canvas, pixel: Pixel) -> None:
        super().__init__()
        self.canvas = canvas
        self.pixel = pixel


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
                row.append(Pixel(pos=Offset(x=j, y=i)))
            self.data.append(row)
        self.mouse_captured = False

    def compose(self):
        for row in self.data:
            yield Horizontal(*row)

    def get_content_width(self, container, viewport) -> int:
        return self.canvas_size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self.canvas_size.height

    def on_pixel_click(self, message):
        print("pixel_click")
        message.stop()
        self.post_message(CanvasClick(canvas=self, pixel=message.pixel))
        self.capture_mouse()
        self.mouse_captured = True

    def on_mouse_move(self, event):
        if not self.mouse_captured:
            return
        if (
            event.x < 0
            or event.y < 0
            or event.x >= len(self.data)
            or event.y >= len(self.data[0])
        ):
            return
        print("mouse_move", event.x, event.y)
        event.stop()
        pixel = self.data[event.y][event.x]
        self.post_message(CanvasClick(canvas=self, pixel=pixel))

    def on_mouse_up(self, event):
        print("mouse_up")
        self.release_mouse()
        self.mouse_captured = False
