from textual.geometry import Size
from textual.widget import Widget
from window_manager.size_state import SizeState


class App(Widget):

    DEFAULT_CSS = """
      App {
        width: auto;
        height: auto;
      }

    """

    title: str = "App"
    preferred_state: SizeState = SizeState.restored
    AUTO_FOCUS = None

    def restored_size(self, new_size: Size):
        window_proportion = Size(0.5, 0.5)
        width = window_proportion.width * new_size.width
        height = window_proportion.height * new_size.height
        return Size(width, height)

    def get_content_width(
            self,
            container,
            viewport,
            content_fraction=None
    ) -> int:
        print(container, viewport, content_fraction)
        if self.is_mounted:
            return container.width

        if self.size_state in [SizeState.maximized, SizeState.fullscreen]:
            return container.width
        return self.restored_size(container).width

    def get_content_height(
            self,
            container,
            viewport,
            content_fraction=None
    ) -> int:
        print(container, viewport, content_fraction)
        if self.is_mounted:
            return container.height

        if self.size_state in [SizeState.maximized, SizeState.fullscreen]:
            return container.height
        return self.restored_size(container).height

    pass
