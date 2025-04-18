from textual.containers import Grid
from textual.geometry import Size
from textual.widget import Widget
from textual.widgets import Static

from window_manager.border import Border
from window_manager.border_style import BorderStyle
from window_manager.size_state import SizeState


class WindowButton(Static):

    symbol: str

    def render(self):
        return self.symbol

    def get_content_width(self, container, viewport) -> int:
        return 1

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return 1


class MinButton(WindowButton):
    symbol = ""


class MaxButton(WindowButton):
    symbol = ""


class RestoreButton(WindowButton):
    symbol = ""


class CloseButton(WindowButton):
    symbol = ""
    DEFAULT_CSS = """
    CloseButton:hover {
      background: #e81123;
    }

    """


class TitleBar(Widget):

    DEFAULT_CSS = """
    TitleBar {
      layout: grid;
      grid-columns: 1fr auto auto auto;
      grid-size: 4;
      padding-left: 1;
      background: #0067dc;
      height: 1;
      width: 100%;
      text-style: bold;

      WindowButton {
        padding: 0 1;
      }
    }

    """

    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def on_mouse_down(self, event):
        self.window.drag_start()

    def compose(self):
        yield Static(self.title)
        yield MinButton()
        if self.parent.state == SizeState.maximized:
            yield RestoreButton()
        else:
            yield MaxButton()

        yield CloseButton()


"""
------------Border.-top------------
|<           TitleBar            >|
|/                               \|
||             Body              ||
|\                               /|
----------Border.-bottom-----------
"""


class Decoration(Grid):

    DEFAULT_CSS = """
    Decoration {
      layout: vertical;

      Border {
        background: transparent;

        &.-top {
          dock: top;
        }

        &.-left {
          dock: left;
        }

        &.-right {
          dock: right;
        }

        &.-bottom {
          dock: bottom;
        }
      }
    }
    """

    def __init__(
        self,
        body: Widget,
        title: str | None,
        state: SizeState | None = SizeState.restored
    ):
        if title is None:
            title = "New Window"
        self.bar = TitleBar(title)
        self.top_border = Border("top")
        self.left_border = Border("left")
        self.right_border = Border("right")
        self.bottom_border = Border("bottom")
        self.body = body
        self.state = state
        super().__init__()
        self.set_border_style(BorderStyle())

    def set_border_style(self, style):
        for border in [self.top_border,
                       self.bottom_border,
                       self.left_border,
                       self.right_border]:
            border.set_border_style(style)

    def on_mount(self):
        self.bar.window = self.parent

    def update_size(self, region):
        styles = self.styles
        styles.height = region.height
        styles.width = region.width
        styles.offset = region.offset

    def compose(self):
        if self.state == SizeState.restored:
            yield self.top_border
            yield self.left_border
            yield self.bar
            yield self.body
            yield self.right_border
            yield self.bottom_border
        elif self.state == SizeState.maximized:
            yield self.bar
            yield self.body
        elif self.state == SizeState.fullscreen:
            yield self.body
