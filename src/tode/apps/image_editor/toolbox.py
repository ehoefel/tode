from textual.containers import Grid, Vertical
from textual.geometry import Size
from textual.reactive import reactive
from textual.widget import Widget

from .tools.color_area import ColorArea
from .tools.tool import Empty
from .tools import tool_list
from .tabs import Tab, TabBar


class Toolbox(Widget):

    DEFAULT_CSS = """
      Toolbox {
        dock: left;
        layout: vertical;
        width: auto;
        height: 100%;
        background: #434343;
        padding-top: 3;
        align: center middle;
        & > Grid {
          width: 100%;
          height: auto;
          grid-size: 5;
          grid-gutter: 0;
          padding: 0;
          grid-columns: auto;
          & > Tool {
            margin: 0;
            color: #bebebe;
            height: auto;
            width: auto;
            padding-left: 1;
          }
        }
        & > Vertical {
          width: 100%;
        }
      }
    """

    active_tool = reactive(None, recompose=True)
    active_tab_idx: int = reactive(None)

    def __init__(self, tools: dict, active_tool: Widget | None):
        super().__init__()
        tool_options_content = Empty()
        if active_tool is not None:
            tool_options_content = active_tool.tool_options
        self.tabs = [
            Tab(name="", content=tool_options_content),
            Tab(name="", content=Widget()),
            Tab(name="", content=Widget()),
            Tab(name="", content=Widget())
        ]
        self.tab_bar = TabBar(*self.tabs, active_tab_idx=self.active_tab_idx)
        self.tools = tools
        self.active_tool = active_tool
        self.active_tab_idx = 0

    def watch_active_tool(self, old_value, new_value) -> None:
        if new_value is None:
            content = Empty()
        else:
            content = new_value.tool_options
        self.tabs[0].content = content

    def watch_active_tab_idx(self, old_value, new_value) -> None:
        for idx, tab in enumerate(self.tabs):
            if idx == new_value:
                tab.content.styles.display = "block"
            else:
                tab.content.styles.display = "none"
        if hasattr(self, "tab_bar"):
            self.tab_bar.active_tab_idx = new_value

    def compose(self):
        map = tool_list
        with Grid():
            tool_classes = self.tools.keys()
            for tool in map:
                if tool in tool_classes:
                    yield self.tools[tool]
                else:
                    yield tool(disabled=True)
        yield self.tools[ColorArea]
        with Vertical():
            yield self.tab_bar
            for tab in self.tabs:
                yield tab.content

    def on_tab_focus(self, event):
        event.stop()
        self.active_tab_idx = event.tab_idx

    def get_content_width(self, container, viewport) -> int:
        return 16

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height
