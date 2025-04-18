from textual.color import Color
from textual.containers import Grid, Horizontal
from textual.geometry import Size
from textual.reactive import reactive
from textual.widget import Widget

from .tabs import Tab, TabBar


class Dialog2(Widget):

    DEFAULT_CSS = """
      Dialog2 {
        height: 1fr;
        background: red 50%;
        outline: round black;

      }

    """


class Dialog1(Widget):

    DEFAULT_CSS = """
      Dialog1 {
        height: 10;
      }

    """

    active_tab_idx: int = reactive(None, recompose=True)

    def __init__(self):
        super().__init__()
        self.active_tab_idx = 0

    def compose(self):
        yield TabBar(
            Tab(name="󰏘", content=Widget()),
            Tab(name="󱀍", content=Widget()),
            active_tab_idx=self.active_tab_idx
        )

    def on_tab_focus(self, event):
        event.stop()
        self.active_tab_idx = event.tab_idx


class RightDock(Widget):

    DEFAULT_CSS = """
    RightDock {
      dock: right;
      height: 100%;
      width: auto;
      padding-top: 1;
    }

    """

    def compose(self):
        yield Dialog1()
        yield Dialog2()

    def get_content_width(self, container, viewport) -> int:
        return 15

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height
