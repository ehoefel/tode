# cSpell:disable

from textual.color import Color
from textual.geometry import Size

from .image import Image
from .right_dock import RightDock
from .toolbox import Toolbox
from .tools import Pencil
from .tools.color_picker import ColorPicker
from .tools.color_area import ColorArea
from .tools.brush_selector import BrushSelector
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
        self.tools[ColorArea] = ColorArea(
            fg=self.memory['fg'],
            bg=self.memory['bg']
        )
        self.tools[BrushSelector] = BrushSelector(value=self.memory['brush'])
        self.tools[Pencil] = Pencil(self.tools[ColorArea])
        self.toolbox = Toolbox(self.tools, active_tool=self.active_tool)
        self.workspace = Workspace()
        self.right_dock = RightDock(
            color_picker=ColorPicker(
                value=self.memory[self.memory['active_color']]
            ),
            brush_selector=self.tools[BrushSelector]
        )

    def on_tool_selected(self, event) -> None:
        event.stop()
        if self.active_tool is not None:
            self.active_tool.pressed = False
        self.active_tool = event.tool
        self.active_tool.pressed = True
        self.toolbox.active_tool = event.tool

    def on_brush_selected(self, event):
        event.stop()
        self.memory['brush'] = event.brush
        self.tools[Pencil].brush = event.brush
        self.toolbox.refresh(recompose=True)

    def on_color_picked(self, event):
        event.stop()
        color_area = self.tools[ColorArea]
        if self.memory['active_color'] == "fg":
            color_area.fg = event.color
        if self.memory['active_color'] == "bg":
            color_area.bg = event.color

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
        image_size = Size(50, 20)
        background = self.memory['bg']
        image = Image.new(image_size, background)
        self.workspace.new_tab(image)

    def on_canvas_click(self, message) -> None:
        if self.active_tool is not None:
            self.active_tool.apply_to_canvas(message.canvas, message.pixel)
