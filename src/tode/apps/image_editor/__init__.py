# cSpell:disable

# from textual.reactive import reactive
# from textual.message import Message

from textual.geometry import Size

from .canvas import Canvas
from .toolbox import Toolbox

from window_manager.menu_bar import MenuBar, MenuItem
from window_manager.size_state import SizeState

from apps.app import App


class ImageEditor(App):

    DEFAULT_CSS = """
    ImageEditor {
      background: #434343;
      & > MenuBar {
        background: #494949;
        &:focus {
          background: #0b0b0b;
        }
      }
    }

    """

    title = "Image Editor"
    preferred_state = SizeState.maximized

    def compose(self):
        yield Toolbox()
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
        yield Canvas(size=Size(50, 20))
