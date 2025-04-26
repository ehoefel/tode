from textual.widget import Widget

from ..image import Image


class Layers(Widget):

    def __init__(self, image: Image | None = None):
        super().__init__()
        self.image = image
