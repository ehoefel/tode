from textual.geometry import Size
from textual.message import Message
from textual.widget import Widget


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


class Tool(Widget):

    symbol: str
    tool_options: Widget = Empty()

    def render(self):
        return self.symbol

    def get_content_width(self, container, viewport) -> int:
        return 1

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return 1

    def on_click(self, event):
        self.post_message(ToolSelected(self))
