from textual.geometry import Size
from textual.widget import Widget

from ..tabs import Tab, TabArea


class Panel(Widget):
    pass


class RightDock(Widget):

    DEFAULT_CSS = """
    RightDock {
      dock: right;
      height: 100%;
      width: auto;
      padding-top: 1;
      background: #3B3B3B;
      layout: grid;
      grid-size: 1;
      grid-rows: auto 1fr;
      grid-gutter: 1;
      hatch: "▄" #454545;
      TabArea {
        height: 1fr;
      }
    }
    """

    def __init__(
        self,
        color_picker: Widget,
        brush_selector: Widget,
        layers: Widget
    ) -> None:
        super().__init__()
        tabs_1 = [
            Tab(name="󰏘", content=color_picker),
            Tab(name="󰛖", content=brush_selector)
        ]
        tabs_2 = [
                Tab(name="󰌨", content=layers),
                Tab(name="󰕭", content=Widget()),
                Tab(name="󰕙", content=Widget())
                ]
        self.tab_area_1 = TabArea(tabs=tabs_1)
        self.tab_area_2 = TabArea(tabs=tabs_2, classes="second")

    def compose(self):
        yield self.tab_area_1
        yield self.tab_area_2

    def get_content_width(self, container, viewport) -> int:
        return 25

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return container.height
