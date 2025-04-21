# cSpell:disable

from textual.color import Color
from textual.geometry import Size

from .toolbox import Toolbox
from .tools import Pencil
from .right_dock import RightDock
from .workspace import Workspace
from .tools.color_picker import ColorPicker
from .tools.active_colors import ActiveColors
from .tools.brush_selector import BrushSelector

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
    active_tool = None
    AUTO_FOCUS = None

    def __init__(self):
        super().__init__()
        self.memory['active_color'] = "fg"
        self.memory['brush'] = " "
        self.memory['fg'] = Color.parse("black")
        self.memory['bg'] = Color.parse("white")
        self.tools[ActiveColors] = ActiveColors(
            fg=self.memory['fg'],
            bg=self.memory['bg']
        )
        self.tools[BrushSelector] = BrushSelector(value=self.memory['brush'])
        self.tools[Pencil] = Pencil()
        self.toolbox = Toolbox(self.tools, active_tool=self.active_tool)
        self.workspace = Workspace()
        self.right_dock = RightDock(
            color_picker=ColorPicker(
                target=self.memory['active_color'],
                value=self.memory[self.memory['active_color']]
            ),
            brush_selector=self.tools[BrushSelector]
        )

    def on_tool_selected(self, event) -> None:
        event.stop()
        self.active_tool = event.tool
        self.active_tool.add_class("-active")
        self.toolbox.active_tool = event.tool

    def on_brush_selected(self, event):
        event.stop()
        self.memory['brush'] = event.brush
        self.tools[Pencil].brush = event.brush
        self.toolbox.refresh(recompose=True)

    def on_color_picked(self, event):
        event.stop()
        active_colors = self.tools[ActiveColors]
        if self.memory['active_brush'] == "fg":
            active_colors.fg = event.color
        if self.memory['active_brush'] == "bg":
            active_colors.bg = event.color

    def compose(self):
        yield self.toolbox
        yield self.workspace
        yield self.right_dock
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
