from textual.geometry import Size
from textual.message import Message
from textual.widget import Widget

from .active_colors import ActiveColors
from apps.image_editor.canvas import Canvas
from apps.image_editor.pixel import Pixel

from utils.button import Button


class ToolOptions(Widget):
    title: str

    def render(self):
        return self.title

    def get_content_width(self, container, viewport) -> int:
        return container.size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container


class Empty(ToolOptions):
    title = "Select a tool"
    pass


class ToolSelected(Message):

    def __init__(self, tool: Widget) -> None:
        super().__init__()
        self.tool = tool


class Tool(Button):

    symbol: str
    tool_options: Widget = Empty()
    active_colors: ActiveColors

    def __init__(
        self,
        active_colors: ActiveColors | None = None,
        *,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=self.symbol, id=id, classes=classes, disabled=disabled)
        self.active_colors = active_colors

    def on_click(self, event):
        self.post_message(ToolSelected(self))

    def apply_to_canvas(self, canvas: Canvas, pixel: Pixel) -> None:
        pass
