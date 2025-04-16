from textual.containers import Grid
from textual.widgets import Static
from border import Border
from border_style import BorderStyle


class Bar(Static):

    def __init__(self):
        super().__init__("bar")

    def on_mouse_down(self, event):
        self.window.drag_start()


"""
------------Border.-top------------
|<              Bar              >|
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

      Bar {
        background: red;
        height: 1;
        width: 100%;
      }

      Placeholder {
        min-height: 5;
      }
    }
    """

    def __init__(self, body):
        self.bar = Bar()
        self.top_border = Border("top")
        self.left_border = Border("left")
        self.right_border = Border("right")
        self.bottom_border = Border("bottom")
        self.body = body
        super().__init__(
            self.top_border,
            self.left_border,
            self.bar,
            self.body,
            self.right_border,
            self.bottom_border
        )
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
