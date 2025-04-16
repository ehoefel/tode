from textual.screen import ModalScreen
from textual.widgets import Placeholder
from textual.geometry import Size, Region, Offset
from decoration import Decoration
from enum import Enum


class Operation(str, Enum):
    dragging = "dragging"
    expanding_left = "expanding_left"
    expanding_right = "expanding_right"
    expanding_top = "expanding_top"
    expanding_bottom = "expanding_bottom"


class Window(ModalScreen):

    DEFAULT_CSS = """
    Window {
      background: transparent;
    }
    """

    def __init__(self, size):
        self.body = Placeholder("window")
        self.decorator = Decoration(self.body)
        super().__init__(self.decorator)
        self.app_size = size
        self.operation = None

    def on_app_resize(self, event):
        print(event)

    def on_mount(self):
        self.default_size()

    def default_size(self):
        window_proportion = Size(0.5, 0.5)
        width = window_proportion.width * self.app_size.width
        height = window_proportion.height * self.app_size.height
        x = int((self.app_size.width - width) / 2)
        y = int((self.app_size.height - height) / 2)
        self._region = Region(x=x, y=y, width=width, height=height)
        self.on_region_update()

    def move(self, amount):
        old_offset = self._region.offset
        x = old_offset.x + amount.x
        y = old_offset.y + amount.y
        new_offset = Offset(x=x, y=y)
        self._region = Region.from_offset(new_offset, size=self._region.size)
        self.on_region_update()

    def on_region_update(self):
        self.decorator.update_size(self._region)

    def compose(self):
        yield self.decorator

    def on_mouse_move(self, event):
        if self.operation == Operation.dragging:
            self.drag_move(event)

    def on_mouse_up(self, event):
        self.operation = None

    def drag_start(self):
        if self.operation is not None:
            return
        self.operation = Operation.dragging

    def drag_move(self, event):
        if self.operation is not Operation.dragging:
            return
        movement = Offset(event.delta_x, event.delta_y)
        self.move(movement)
