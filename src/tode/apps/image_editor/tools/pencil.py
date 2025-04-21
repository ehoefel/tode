from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from .tool import Tool, ToolOptions


class FormLine(Widget):
    DEFAULT_CSS = """
    FormLine {
      layout: grid;
      grid-size: 2;
      grid-rows: 1;
      grid-columns: 1fr 1;
    }
    """

    label: str
    value: Widget

    def compose(self):
        yield Static(self.label)
        yield self.value


class BrushLine(FormLine):
    label = "brush: "
    value = Static(" ")


class Checkbox(Widget):
    #  󰄮 󰡖 󰄲 󰱒  󰄱 󰄵
    #  󰄱  󰄱 󰄱  󰄱 󰄵

    checked = reactive(False)

    def __init__(self, checked: bool = False):
        super().__init__()
        self.checked = checked

    def render(self):
        return "󰄲 " if self.checked else "󰄱 "

    def on_click(self, event):
        self.checked = not self.checked


class PaintBackgroundOption(FormLine):

    checked = reactive(False)
    label = "background: "

    def __init__(self, checked: bool = False):
        super().__init__()
        self.checked = checked
        self.value = Checkbox(checked=self.checked)


class PencilToolOptions(ToolOptions):
    title = "Pencil"

    brush = reactive(" ")

    def __init__(self, brush: str | None = " ") -> None:
        super().__init__()
        self.brush_line = BrushLine()
        self.paint_background_option = PaintBackgroundOption()
        self.brush = brush

    def watch_brush(self, old_value, new_value) -> None:
        self.brush_line.value.update(new_value)

    def compose(self):
        yield self.brush_line
        yield self.paint_background_option


class Pencil(Tool):
    symbol = ""
    tool_options = PencilToolOptions()
    brush = reactive(" ")

    def watch_brush(self, old_value, new_value) -> None:
        self.tool_options.brush = new_value
