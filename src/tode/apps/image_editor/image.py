from textual.color import Color
from textual.reactive import reactive
from textual.geometry import Size
from textual.widget import Widget

from .canvas import Canvas, Layer


class Image(Widget):

    DEFAULT_CSS = """
      Image {
        width: auto;
        height: auto;
      }
    """

    image_size: Size
    canvas: Canvas
    _layers: list = reactive(None)

    def __init__(
        self,
        name: str,
        size: Size,
        layers: list | None = None
    ) -> None:
        super().__init__(name=name)
        self.image_size = size
        if layers is None:
            layers = []
        self.canvas = Canvas(size, layers)
        self._layers = layers

    def watch__layers(self, old_value, new_value) -> None:
        self.canvas._layers = new_value

    def new(size: Size, background: Color | None = None):
        name = "Untitled.xcf"
        image = Image(name=name, size=size)
        if background is not None:
            layer_name = "Background"
            layer = Layer.fill_with(layer_name, size, background)
            image._layers.append(layer)
        return image

    def compose(self):
        yield self.canvas

    def get_content_width(self, container, viewport) -> int:
        return self.image_size.width

    def get_content_height(self, container: Size, viewport: Size, width: int):
        return self.image_size.height
