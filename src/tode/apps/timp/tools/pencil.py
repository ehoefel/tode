from textual.geometry import Offset
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Static

from ..utils.checkbox import Checkbox

from ..image.canvas import Layer
from ..image.pixel import Pixel
from .tool import Tool, ToolOptions


class FormLine(Widget):
    DEFAULT_CSS = """
    FormLine {
      layout: grid;
      grid-size: 2;
      grid-rows: 1;
      grid-columns: 1fr auto;
      height: 1;
      padding: 0 1;
      Static.label {
        width: 1fr;
      }
      Static.value {
        text-align: right;
        width: 100%;
      }
    }
    """

    label: str
    value: Widget

    def compose(self):
        self.value.add_class("value")
        yield Static(self.label, classes="label")
        yield self.value


class BrushLine(FormLine):
    label = "brush: "
    value = Static(" ")


class PaintBackgroundOption(FormLine):
    DEFAULT_CSS = """

    """

    checked = var(False)
    label = "background: "

    def __init__(self, checked: bool = False):
        super().__init__()
        self.value = Checkbox(checked=checked)
        self.checked = checked

    def watch_checked(self, old_value, new_value):
        self.value.checked = new_value

    def on_checkbox_changed(self, message) -> None:
        self.checked = message.value
        message.stop()


class PencilToolOptions(ToolOptions):
    title = "Pencil"

    brush = var(" ")

    def __init__(self, brush: str | None = " ") -> None:
        super().__init__()
        self.brush_line = BrushLine()
        self.paint_background = PaintBackgroundOption()
        self.brush = brush

    def watch_brush(self, old_value, new_value) -> None:
        self.brush_line.value.update(new_value)

    def compose(self):
        yield self.brush_line
        yield self.paint_background


class Pencil(Tool):
    symbol = ""
    tool_options = PencilToolOptions()
    brush = var(Pixel.BLANK)

    def watch_brush(self, old_value, new_value) -> None:
        self.tool_options.brush = new_value

    def apply_to_layer(self, layer: Layer, pos: Offset) -> None:
        char = self.brush
        fg = self.color_area.fg
        bg = self.color_area.bg
        if not self.tool_options.paint_background.value.checked:
            bg = None
        pixel = Pixel(char=char, fg=fg, bg=bg)
        layer.apply(pos, pixel)
