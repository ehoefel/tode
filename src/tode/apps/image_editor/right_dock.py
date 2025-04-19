from textual.geometry import Size
from textual.reactive import reactive
from textual.widget import Widget

from .tools.color_picker import ColorPicker
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
        height: auto;
      }

    """

    active_tab_idx: int = reactive(None, recompose=True)

    def __init__(self, color_picker: Widget):
        super().__init__()
        self.active_tab_idx = 0
        self.color_picker = color_picker
        self.tabs = [
            Tab(name="󰏘", content=self.color_picker),
            Tab(name="󱀍", content=Widget()),
        ]

    def compose(self):
        yield TabBar(*self.tabs, active_tab_idx=self.active_tab_idx)
        if self.active_tab_idx is not None:
            yield self.tabs[self.active_tab_idx].content

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

    def __init__(self, color_picker: Widget):
        super().__init__()
        self.color_picker = color_picker

    def compose(self):
        yield Dialog1(self.color_picker)
        # yield Dialog2()

    def get_content_width(self, container, viewport) -> int:
        return 15

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height
