from textual.color import Color
from textual.message import Message
from textual.geometry import Size, Offset
from textual.reactive import var, reactive
from textual.widget import Widget

from .canvas import Canvas, Layer, CanvasClick, LayerUpdate, LayerView


class ImageClick(Message):

    def __init__(self, layer: Layer | None, pos: Offset) -> None:
        super().__init__()
        self.layer = layer
        self.pos = pos


class Image(Widget):

    DEFAULT_CSS = """
      Image {
        width: auto;
        height: auto;
      }
    """

    def new(size: Size, background: Color | None = None):
        name = "Untitled.xcf"
        image = Image(name=name, size=size)
        if background is not None:
            layer_name = "Background"
            image.create_layer(layer_name, size, background)
        return image

    image_size: Size
    canvas: Canvas
    _layers: var[dict[str, Layer]] = var(None)
    layer_order: var[list[str]] = var(None)
    active_layer_name: var[str] = var(None)
    views: var[dict[str, LayerView]] = reactive(None)

    def __init__(
        self,
        name: str,
        size: Size,
        layers: dict[str, Layer] | None = None,
        layer_order: list[str] | None = None,
        active_layer_name: str | None = None
    ) -> None:
        super().__init__(name=name)
        self.image_size = size
        if layers is None:
            layers = dict()
            layer_order = list()
        elif layer_order is None:
            layer_order = layers.keys()
        self.canvas = Canvas(size)
        self.set_reactive(Image._layers, layers)
        self.set_reactive(Image.layer_order, layer_order)
        self.set_reactive(Image.views, dict())

        canvas_view = LayerView(size, base=None, layer=self.canvas)
        self.create_view(self.canvas.name, canvas_view)

        if len(layers) > 0 and active_layer_name is None:
            active_layer_name = layers[-1].name
        self.set_reactive(Image.active_layer_name, active_layer_name)

    def create_view(self, view_name, view):
        self.views[view_name] = view
        self.mutate_reactive(Image.views)

    def create_layer(
        self,
        name: str | None = None,
        size: Size | None = None,
        background: Color | None = None,
        data: list | None = None
    ) -> None:
        if name in self._layers.keys():
            i = 1
            while name := f'{name} #{i}' in self._layers.keys():
                i += 1

        if background is not None:
            layer = Layer.fill_with(name, size, background)
        else:
            layer = Layer(name, size, data)
        layer.post_message = self.post_message

        self._layers[name] = layer
        self.layer_order.append(name)
        self.active_layer_name = name

        layer_index = self.layer_order.index(name)
        if layer_index == 0:
            previous_view = self.views[self.canvas.name]
        else:
            previous_layer_name = self.layer_order[layer_index - 1]
            previous_view = self.views[previous_layer_name]

        view = LayerView(self.image_size, previous_view, layer)
        self.create_view(name, view)

    @property
    def active_layer(self):
        if self._layers is None or self.active_layer_name is None:
            return None
        return self._layers[self.active_layer_name]

    @property
    def active_view(self):
        for name in reversed(self.layer_order):
            if self._layers[name].visible:
                return self.views[name]
        return self.views[self.canvas.name]

    def watch_views(self, old_value, new_value) -> None:
        self.canvas.view = self.active_view

    def compose(self):
        yield self.canvas

    def on_layer_update(self, message: LayerUpdate) -> None:
        layer_idx = self.layer_order.index(message.layer.name)
        # iterate through a list of pairs (prev, curr) of adjacent layers
        # the prev of self._layers[0] is None
        # the first curr is self._layers[layer_idx]
        for name in self.layer_order[layer_idx:]:
            self.views[name].update(message)
        if message.region is None:
            self.canvas.refresh()
        else:
            self.canvas.refresh(message.region)

    def get_content_width(self, container, viewport) -> int:
        return self.image_size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self.image_size.height

    def on_canvas_click(self, message: CanvasClick):
        pos = message.pos
        layer = self.active_layer
        print(pos, layer, self.active_layer_name)
        self.post_message(ImageClick(layer=layer, pos=pos))
        # top_layer = self.active_layer
