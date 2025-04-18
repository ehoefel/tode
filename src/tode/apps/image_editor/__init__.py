# cSpell:disable

# from textual.reactive import reactive
# from textual.message import Message

from textual.geometry import Size

from .canvas import Canvas
from .toolbox import Toolbox
from .right_dock import RightDock
from .workspace import Workspace

from window_manager.menu_bar import MenuBar, MenuItem
from window_manager.size_state import SizeState

from apps.app import App


class ImageEditor(App):

    DEFAULT_CSS = """
    ImageEditor {
      layout: vertical;
      width: 1fr;
      height: 1fr;

      & > MenuBar {
        dock: top;
        background: #494949;
        MenuItem {
          color: white;
        }
      }

      Workspace {
        background: #434343;
      }
    }

    """

    title = "Image Editor"
    preferred_state = SizeState.maximized

    def compose(self):
        yield Toolbox()
        yield Workspace()
        yield RightDock()
        yield MenuBar(
            MenuItem("File"),
            MenuItem("Edit"),
            MenuItem("Select"),
            MenuItem("Image"),
            MenuItem("Layer"),
            MenuItem("Colors"),
            MenuItem("Filters"),
            MenuItem("Windows"),
            MenuItem("Help")
        )

    def on_mount(self):
        canvas_size = Size(50, 20)
        canvas_name = "Untitled.xcf"
        self.get_child_by_type(Workspace).new_tab(canvas_name, canvas_size)
