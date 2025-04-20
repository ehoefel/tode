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

    active_tab_idx: int = reactive(None)

    def __init__(self, color_picker: Widget, brush_selector: Widget):
        super().__init__()
        self.color_picker = color_picker
        self.brush_selector = brush_selector
        self.tabs = [
            Tab(name="󰏘", content=self.color_picker),
            Tab(name="󱀍", content=self.brush_selector)
        ]
        self.active_tab_idx = 0

    def watch_active_tab_idx(self, old_value, new_value) -> None:
        for idx, tab in enumerate(self.tabs):
            if idx == new_value:
                tab.content.styles.display = "block"
            else:
                tab.content.styles.display = "none"
        if self.is_mounted:
            self.get_child_by_type(TabBar).active_tab_idx = new_value

    def compose(self):
        yield TabBar(*self.tabs, active_tab_idx=self.active_tab_idx)
        for tab in self.tabs:
            yield tab.content

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

    def __init__(self, color_picker: Widget, brush_selector: Widget):
        super().__init__()
        self.color_picker = color_picker
        self.brush_selector = brush_selector

    def compose(self):
        yield Dialog1(self.color_picker, self.brush_selector)
        # yield Dialog2()

    def get_content_width(self, container, viewport) -> int:
        return 15

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height
