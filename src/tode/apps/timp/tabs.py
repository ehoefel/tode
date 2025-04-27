from typing import Iterable

from textual.widget import Widget
from textual.reactive import reactive, var
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
      background: #202020;
      &.-active {
        background: #3B3B3B;
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


class TabBar(Widget):

    DEFAULT_CSS = """
      TabBar {
        dock: top;
        layout: horizontal;
        height: auto;
        background: #454545;
      }
    """

    active_tab_idx: int = reactive(0)

    def __init__(self, *tabs: Iterable[Tab], active_tab_idx: int) -> None:
        super().__init__()
        self.tabs = tabs
        self.active_tab_idx = active_tab_idx

    def watch_active_tab_idx(self, old_value, new_value) -> None:
        for idx, tab in enumerate(self.tabs):
            if idx == new_value:
                tab.add_class("-active")
            else:
                tab.remove_class("-active")

    def compose(self):
        for tab in self.tabs:
            yield tab

    def on_tab_focus(self, event):
        """ receive a TabFocus message sent by a tab
        stop that message
        send another TabFocus message with the index of the tab
        from the first event
        """
        event.tab_idx = self.tabs.index(event.tab)


class TabArea(Widget):

    DEFAULT_CSS = """
    TabArea {
      height: 100%;
    }

    """

    tabs: var[list[Tab]] = var(None)
    active_tab_idx: var[int] = var(None)

    def __init__(
        self,
        tabs: list[Tab],
        active_tab_idx: int | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

        if active_tab_idx is None:
            active_tab_idx = 0

        self.tab_bar = TabBar(*tabs, active_tab_idx=active_tab_idx)
        self.set_reactive(TabArea.tabs, tabs)
        self.active_tab_idx = active_tab_idx

    def watch_active_tab_idx(self, old_value, new_value) -> None:
        for idx, tab in enumerate(self.tabs):
            if idx == new_value:
                tab.content.styles.display = "block"
            else:
                tab.content.styles.display = "none"
        self.tab_bar.active_tab_idx = new_value

    def compose(self):
        yield self.tab_bar
        for tab in self.tabs:
            yield tab.content

    def on_tab_focus(self, event):
        event.stop()
        self.active_tab_idx = event.tab_idx
