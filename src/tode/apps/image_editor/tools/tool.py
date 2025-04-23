from textual.geometry import Size, Offset
from textual.message import Message
from textual.widget import Widget

from .color_area import ColorArea
from apps.image_editor.canvas import Layer

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
    color_area: ColorArea

    def __init__(
        self,
        color_area: ColorArea | None = None,
        *,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=self.symbol, id=id, classes=classes, disabled=disabled)
        self.color_area = color_area

    def on_click(self, event):
        self.post_message(ToolSelected(self))

    def apply_to_layer(self, layer: Layer, pos: Offset) -> None:
        pass
