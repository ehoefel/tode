from typing import Iterable

from rich.console import Console, ConsoleOptions
from rich.segment import Segment

from textual.css.query import NoMatches
from textual.reactive import var, reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Static, ListView, ListItem

from ..image import Image
from ..image.layer import Layer

from .footer import Footer, FooterButton


class Layers(Widget):

    class LayerItem(ListItem):

        VISIBLE_ICON = ""      #   󰈈      󰛐
        NOT_VISIBLE_ICON = ""  #   󱀦 󰈉 󱗣  󱀧 󰛑 󱗤
        LINK_ICON = ""         # 󰌷󰌹󰿨
        NO_LINK_ICON = ""      # 󰌷󰌹󰿨

        COMPONENT_CLASSES = ("-active",)

        DEFAULT_CSS = """
        LayerItem {
          layout: horizontal;
          width: 100%;
          height: 1;
          padding-left: 1;
          &.-highlight {
            color: white !important;
            background: #1F1F1F !important;
            text-style: none !important;
          }
          & > Static {
            width: auto;
            height: 1;
          }

          .link {
            padding-left: 1;
          }
          .name {
            padding-left: 4;
          }
        }

        """

        active: reactive[bool] = reactive(False)
        visible: reactive[bool] = reactive(False)
        linked: reactive[bool] = reactive(False)

        def __init__(
            self,
            layer: Layer,
            id: str | None = None
        ) -> None:
            super().__init__(name=layer.name, id=id)
            self.visibility = Static(Layers.LayerItem.VISIBLE_ICON,
                                     classes="visibility")
            self.linked = Static(Layers.LayerItem.LINK_ICON, classes="link")
            self.text = Static(layer.name, classes="name")

        def watch_active(self, old_value, new_value):
            self.highlighted = new_value

        def compose(self):
            yield self.visibility
            yield self.linked
            yield self.text

    class LayerList(ListView):

        DEFAULT_CSS = """
          LayerList {
            layout: vertical;
            height: 1fr;
            width: 1fr;
            background: #303030;
          }

        """

        _layers: reactive[list[Layer] | None] = reactive(None, recompose=True)
        layer_order: reactive[list[str] | None] = reactive(None, recompose=True)
        active_layer_name: var[str | None] = var(None)

        def __init__(self) -> None:
            super().__init__()

        def watch_active_layer_name(self, old_value, new_value):
            if not self.is_mounted:
                return
            if old_value is not None:
                self.get_child_by_id(old_value).active = False
            if new_value is not None:
                try:
                    self.get_child_by_id(new_value).active = True
                except NoMatches:
                    pass

        def compose(self):
            if self._layers is None or len(self._layers) == 0:
                return
            ordered_layers = [self._layers[name] for name in self.layer_order]
            for layer in ordered_layers:
                item = Layers.LayerItem(layer, id=layer.name)
                item.active = layer.name == self.active_layer_name
                yield item

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
            padding_amount -= len(text_left) + len(text_right)
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
    active_layer_name: var[str] = var(None)

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
            self.active_layer_name = new_value.active_layer_name

    def watch__layers(self, old_value, new_value) -> None:
        pass

    def watch_layer_order(self, old_value, new_value) -> None:
        if new_value is None:
            self.layer_list.items = None
            return
        layers = [self._layers[name] for name in new_value]
        self.layer_list.items = layers

        pass

    def compose(self):
        yield self.mode_select
        yield self.opacity_bar
        yield self.lock
        yield self.layer_list.data_bind(
                _layers=Layers._layers,
                layer_order=Layers.layer_order,
                active_layer_name=Layers.active_layer_name)
        yield self.footer
