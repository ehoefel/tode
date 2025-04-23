from textual.color import Color
from textual.message import Message
from textual.geometry import Size, Offset
from textual.reactive import var
from textual.widget import Widget

from .canvas import Canvas, Layer, CanvasClick


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

    image_size: Size
    canvas: Canvas
    _layers: list = var(None)

    def __init__(
        self,
        name: str,
        size: Size,
        layers: list | None = None,
        active_layer_idx: int | None = None
    ) -> None:
        super().__init__(name=name)
        self.image_size = size
        if layers is None:
            layers = []
        self.canvas = Canvas(size, layers)
        self._layers = layers
        if len(layers) > 0 and active_layer_idx is None:
            active_layer_idx = len(layers) - 1
        self.active_layer_idx = active_layer_idx

    def watch__layers(self, old_value, new_value) -> None:
        self.canvas._layers = new_value
        if new_value is None:
            return
        for i, layer in enumerate(new_value):
            if layer not in old_value:
                self.active_layer_idx = i
                return

    def create_layer(
        self,
        name: str | None = None,
        size: Size | None = None,
        background: Color | None = None,
        data: list | None = None
    ) -> None:
        if background is not None:
            if name is not None:
                name = "Background"
            layer = Layer.fill_with(name, size, background)
        else:
            layer = Layer(name, size, data)
        self._layers = self._layers = [layer]

    def new(size: Size, background: Color | None = None):
        name = "Untitled.xcf"
        image = Image(name=name, size=size)
        if background is not None:
            layer_name = "Background"
            image.create_layer(layer_name, size, background)
        return image

    @property
    def active_layer(self):
        if self._layers is None or self.active_layer_idx is None:
            return None
        return self._layers[self.active_layer_idx]

    def compose(self):
        yield self.canvas

    def get_content_width(self, container, viewport) -> int:
        return self.image_size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self.image_size.height

    def on_canvas_click(self, message: CanvasClick):
        pos = message.pos
        layer = self.active_layer
        self.post_message(ImageClick(layer=layer, pos=pos))
        # top_layer = self.active_layer
