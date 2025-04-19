# cSpell:disable

# from textual.reactive import reactive
# from textual.message import Message

from textual.geometry import Size
from textual.color import Color

from .toolbox import Toolbox
from .right_dock import RightDock
from .workspace import Workspace
from .tools.color_picker import ColorPicker
from .tools.active_colors import ActiveColors

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
    memory = dict()
    tools = dict()
    AUTO_FOCUS = None

    def __init__(self):
        super().__init__()
        self.memory['active_brush'] = "fg"
        self.memory['fg'] = Color.parse("black")
        self.memory['bg'] = Color.parse("white")
        self.tools['active_colors'] = ActiveColors(
            fg=self.memory['fg'],
            bg=self.memory['bg']
        )

    def on_color_picked(self, event):
        event.stop()
        active_colors = self.tools['active_colors']
        if self.memory['active_brush'] == "fg":
            active_colors.fg = event.color
        if self.memory['active_brush'] == "bg":
            active_colors.bg = event.color

    def compose(self):
        yield Toolbox(self.tools)
        yield Workspace()
        yield RightDock(
            color_picker=ColorPicker(
                target=self.memory['active_brush'],
                value=self.memory[self.memory['active_brush']]
                )
            )
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
