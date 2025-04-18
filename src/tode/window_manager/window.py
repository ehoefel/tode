from textual.screen import ModalScreen
from textual.geometry import Size, Region, Offset
from textual.reactive import reactive

from apps.app import App
from window_manager.size_state import SizeState
from window_manager.decoration import Decoration
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

    state: SizeState
    app_region: Region | None = reactive(None)
    title: str | None
    body: App

    def __init__(
        self,
        body: App,
        state: SizeState | None = None
    ) -> None:
        super().__init__()

        if state is None:
            state = body.preferred_state

        self.state = state
        self.app_region = Region()
        self.body = body
        self.operation = None

    def on_resize(self, event):
        size = event.size
        if self.state == SizeState.restored:
            size = self.body.restored_size(event.size)
        self.set_size(size)

    def set_size(self, new_size: Size):
        self.app_region = Region.from_offset(self.app_region.offset, new_size)

    def set_offset(self, new_offset: Offset):
        self.app_region = self.app_region.reset_offset.translate(new_offset)

    def move(self, amount):
        self.app_region = self.app_region.translate(amount)

    def watch_app_region(self, old_values, new_values):
        if self.is_mounted:
            self.get_child_by_type(Decoration).update_size(self.app_region)

    def compose(self):
        yield Decoration(
                self.body,
                title=self.body.title,
                state=self.state
                )

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
