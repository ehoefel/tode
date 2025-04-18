from typing import Iterable

from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message


class TabFocus(Message):

    def __init__(self, tab):
        self.tab = tab
        super().__init__()


class Tab(Widget):

    DEFAULT_CSS = """
     Tab {
      width: auto;
      height: auto;
      padding: 0 1;
      background: #212321;
      &.-active {
        background: #393b39;
      }
     }
    """

    def __init__(self, name: str, content: Widget) -> None:
        super().__init__(name=name)
        self.content = content

    def render(self):
        return self.name

    def on_click(self):
        if self.has_class("-active"):
            return
        self.post_message(TabFocus(tab=self))


class TabBarBottomBorder(Widget):

    DEFAULT_CSS = """
      TabBarBottomBorder {
        dock: bottom;
        height: 1;
        width: 100%;
        color: #565855;
      }
    """

    gap_start: int = reactive(0)
    gap_length: int = reactive(0)

    def __init__(self, tabs, active_tab_idx):
        super().__init__()
        self.tabs = tabs
        self.active_tab_idx = active_tab_idx
        self.calculate_gap_size()

    def calculate_gap_size(self):
        if self.active_tab_idx is None:
            self.gap_start = 0
            self.gap_length = 0
        else:
            active_tab = self.tabs[self.active_tab_idx]
            self.gap_start = 0
            for tab_before in self.tabs[:self.active_tab_idx]:
                self.gap_start += tab_before.outer_size.width
            self.gap_length = active_tab.outer_size.width

    def on_resize(self):
        self.calculate_gap_size()

    def render(self):
        left = "▔" * self.gap_start
        gap = " " * self.gap_length
        right = "▔" * (self.size.width - (len(left) + len(gap)))
        return left + gap + right


class TabBar(Widget):

    DEFAULT_CSS = """
      TabBar {
        dock: top;
        layout: horizontal;
        height: auto;
      }
    """

    def __init__(self, *tabs: Iterable[Tab], active_tab_idx: int) -> None:
        super().__init__()
        self.tabs = tabs
        self.active_tab_idx = active_tab_idx
        for idx, tab in enumerate(self.tabs):
            if idx == active_tab_idx:
                tab.add_class("-active")
            else:
                tab.remove_class("-active")

    def compose(self):
        for tab in self.tabs:
            yield tab
        yield TabBarBottomBorder(self.tabs, self.active_tab_idx)

    def on_tab_focus(self, event):
        """ receive a TabFocus message sent by a tab
        stop that message
        send another TabFocus message with the index of the tab
        from the first event
        """
        event.tab_idx = self.tabs.index(event.tab)

