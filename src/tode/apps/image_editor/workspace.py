from textual.geometry import Size
from textual.reactive import reactive
from textual.widget import Widget
from textual.containers import Container

from .canvas import Canvas
from .tabs import Tab, TabBar


class Ruler(Widget):

    DEFAULT_CSS = """
      Ruler {
        &.-top {
          dock: top;
          width: 100%;
          height: 2;
          border-bottom: tall white;
        }

      }

    """

    def __init__(self, is_top: bool):
        super().__init__()
        self.is_top = is_top

    def on_mount(self):
        if self.is_top:
            self.add_class("-top")


class Workspace(Widget):

    DEFAULT_CSS = """
      Workspace {
        layout: vertical;
      }
    """

    active_tab_idx: int = reactive(None, recompose=True)

    def __init__(self):
        super().__init__()
        self.tabs = []

    def new_tab(self, name: str, size: Size, focus: bool = True):
        canvas = Canvas(size)
        tab = Tab(name, canvas)
        self.tabs.append(tab)
        if self.active_tab_idx is None or focus:
            self.active_tab_idx = len(self.tabs) - 1

    def compose(self):
        with Container():
            if self.active_tab_idx is not None:
                yield self.tabs[self.active_tab_idx].content
            # yield Ruler(is_top=True)

        yield TabBar(*self.tabs, active_tab_idx=self.active_tab_idx)

    def on_tab_focus(self, event):
        event.stop()
        print("got new tab focus", event)
        print(self.active_tab_idx, " -> ", event.tab_idx)
        self.active_tab_idx = event.tab_idx

