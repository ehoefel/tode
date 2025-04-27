from typing import Iterable

from rich.console import Console, ConsoleOptions
from rich.segment import Segment

from textual.reactive import var, reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Static

from ..image import Image
from ..image.canvas import Layer

from .footer import Footer, FooterButton



class Layers(Widget):


    class LayerList(Widget):

        VISIBLE_ICON = ""     #     󰈈      󰛐
        NOT_VISIBLE_ICON = "" #     󱀦 󰈉 󱗣  󱀧 󰛑 󱗤

        DEFAULT_CSS = """
          LayerList {
            layout: vertical;
            height: 1fr;
            width: 1fr;
            background: #303030;
            margin-left: 1;
            padding-left: 1;
          }

        """

        items: reactive[list[Layer] | None] = reactive(None)

        def __init__(self, layers: list[Layer] | None = None) -> None:
            super().__init__()
            self.items = layers

        def render(self):
            return self

        def __rich_console__(
            self, console: Console, options: ConsoleOptions
        ) -> Iterable[Segment]:
            segments = []
            style = self.get_component_rich_style()
            for item in self.items:
                if item.visible:
                  visibility = self.VISIBLE_ICON
                else:
                  visibility = self.INVISIBLE_ICON
                segments.append(Segment(visibility, style=style))
                segments.append(Segment(f' {item.name}', style=style))
                segments.append(Segment.line())
            return segments[:-1]

    class ModeSelect(Widget):

        DEFAULT_CSS = """
          ModeSelect {
            margin: 0 1;
            padding: 0 1;
            height: 1;
            width: 100%;
            background: #2C2C2C;
          }
        """

        def render(self):
            text_left = "Mode"
            text_right = "Normal "
            padding_amount = self.size.width
            padding_amount -= len(text_left) + len(text_right)
            text_padding = " " * padding_amount
            return f'{text_left}{text_padding}{text_right}'

        def get_content_width(self, container, viewport) -> int:
            return container.width

        def get_content_height(self, container, viewport, width):
            return 1

    class OpacityBar(Widget):

        DEFAULT_CSS = """
          OpacityBar {
            margin: 0 1;
            height: 1;
            width: 100%;
            background: #555555;
            color: white;
          }

        """

        def get_content_width(self, container, viewport) -> int:
            return container.width

        def get_content_height(self, container, viewport, width):
            return 1

        def render(self):
            return self

        def __rich_console__(
            self, console: Console, options: ConsoleOptions
        ) -> Iterable[Segment]:
            text_left = "Opacity"
            text_right = "100"
            padding_amount = self.size.width
            padding_amount -=  len(text_left) + len(text_right)
            text_padding = " " * padding_amount
            text = f'{text_left}{text_padding}{text_right}'
            style = self.get_component_rich_style()
            segments = []
            segments.append(Segment(text, style))
            return Strip(segments)

    class Lock(Widget):

        DEFAULT_CSS = """
          Lock {
            margin: 0 1;
            layout: horizontal;
            height: 1;
            width: 100%;
            Static {
              width: auto;
              height: 1;
            }
          }
        """

        def compose(self):
            yield Static("Lock: ")
            yield Static(" ")  # 󰃣 
            yield Static(" ")  # 󰁁  
            yield Static("󰄺 ")


    class NewLayer(FooterButton):
        symbol = "󰹍"

    class NewFolder(FooterButton):
        symbol = "󰉗"  # 󰉗  󰮝 󱑿

    class MoveLayerUp(FooterButton):
        symbol = ""  #    󰅃

    class MoveLayerDown(FooterButton):
        symbol = ""  #     󰅀

    class Duplicate(FooterButton):
        symbol = ""  # 󰆑 

    class Merge(FooterButton):
        symbol = "󰶹"  # 󰶹 󰄼 󰞒 󰶡 󰡍   󰌨  󰽘

    class MaskLayer(FooterButton):
        symbol = "󰴂"

    class RemoveLayer(FooterButton):
        symbol = "󰹎"  # 󰹎 󰌩  

    DEFAULT_CSS = """
      Layers {
        padding-top: 1;
        min-height: 10;
        background: #3B3B3B;  # 󱪾 󰕭
      }

    """

    image: var[Image] = var(None)
    _layers: var[list[Layer]] = var(None)
    layer_order: var[list[int]] = var(None)

    def __init__(self, image: Image | None = None):
        super().__init__()
        self.layer_list = Layers.LayerList()
        self.mode_select = Layers.ModeSelect()
        self.opacity_bar = Layers.OpacityBar()
        self.lock = Layers.Lock()
        self.image = image
        self.footer = Footer(
            Layers.NewLayer(),
            Layers.NewFolder(),
            Layers.MoveLayerUp(),
            Layers.MoveLayerDown(),
            Layers.Duplicate(),
            Layers.Merge(),
            Layers.MaskLayer(),
            Layers.RemoveLayer(),
        )

    def watch_image(self, old_value, new_value) -> None:
        if new_value is not None:
            self._layers = new_value._layers
            self.layer_order = new_value.layer_order

    def watch__layers(self, old_value, new_value) -> None:
        print("layers update", old_value, new_value)
        pass

    def watch_layer_order(self, old_value, new_value) -> None:
        if new_value is None:
            self.layer_list.items = None
            return
        layers = [self._layers[name] for name in new_value]
        self.layer_list.items = layers

        print("layer order update", old_value, new_value)
        pass

    def compose(self):
        yield self.mode_select
        yield self.opacity_bar
        yield self.lock
        yield self.layer_list
        yield self.footer
