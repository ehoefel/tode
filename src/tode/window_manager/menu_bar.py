from textual.widget import Widget


class MenuItem(Widget):

    DEFAULT_CSS = """
    MenuItem {
      height: 1;
      width: auto;
      padding: 0 1;
    }
    """

    def __init__(
        self,
        title: str,
        *menu_items: Widget
    ) -> None:
        super().__init__()
        self.title = title
        self.menu_items = menu_items

    def render(self):
        return self.title


class MenuBar(Widget):

    DEFAULT_CSS = """
    MenuBar {
      layout: horizontal;
      height: 1;
      width: 1fr;
    }
    """

    def __init__(
        self,
        *menu_items: MenuItem,
    ) -> None:
        super().__init__()
        self.menu_items = menu_items

    def compose(self):
        for item in self.menu_items:
            yield item
