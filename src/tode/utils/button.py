from typing import Iterable
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style as RichStyle

from textual.reactive import reactive
from textual.widget import Widget


class Button(Widget):

    COMPONENT_CLASSES = (
        "-normal",
        "-border-top",
        "-border-left",
        "-pressed",
        "-pressed-border-top",
        "-pressed-border-left",
        "-disabled"
    )

    DEFAULT_CSS = """
      $button-color: #CCCCCC;
      $button-border: #999999;
      $button-bg: #656565;
      $button-pressed-color: white;
      $button-pressed-border: #320000;
      $button-pressed-bg: #321515;
      Button {
        width: auto;
        height: auto;
        background: transparent;
        color: $button-color;
      }

      .-normal {
        color: $button-color;
        background: $button-bg;
      }

      .-border-top {
        color: $button-border;
        background: transparent;
      }

      .-border-left {
        color: $button-border;
        background: $button-bg;
      }

      .-pressed {
        color: $button-pressed-color;
        background: $button-pressed-bg;
      }

      .-pressed-border-top {
        color: $button-pressed-border;
        background: transparent;
      }

      .-pressed-border-left {
        color: $button-pressed-border;
        background: $button-pressed-bg;
      }

      .-disabled {
        color: $button-pressed-border;
        background: $button-pressed-bg;
      }

    """

    pressed = reactive(False)

    def __init__(
        self,
        name: str,
        pressed: bool | None = False,
        *,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)

    def watch_pressed(self, old_value, new_value) -> None:
        if new_value:
            self.add_class("-pressed")
        else:
            self.remove_class("-pressed")

    def get_content_width(self, container, viewport) -> int:
        return len(self.name) + 2

    def get_content_height(self, container, viewport, width):
        return 2

    def render(self):
        return self

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        segments = []
        style = self.get_component_rich_style("-normal")
        border_top_style = self.get_component_rich_style("-border-top")
        border_left_style = self.get_component_rich_style("-border-left")
        if self.pressed:
            style = self.get_component_rich_style("-pressed")
            border_top_style = self.get_component_rich_style("-pressed-border-top")
            border_left_style = self.get_component_rich_style("-pressed-border-left")
        if self.disabled:
            style = self.get_component_rich_style("-disabled")
            border_top_style = self.get_component_rich_style("-pressed-border-top")
            border_left_style = self.get_component_rich_style("-pressed-border-left")
        segments.append(Segment("▁▁▁", style=border_top_style))
        segments.append(Segment.line())
        segments.append(Segment("▎", style=border_left_style))
        segments.append(Segment(self.name + " ", style=style))
        return segments
