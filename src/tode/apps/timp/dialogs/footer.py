from typing import Iterable

from rich.console import Console, ConsoleOptions
from rich.segment import Segment

from textual.widget import Widget


class FooterButton(Widget):
    symbol: str
    DEFAULT_CSS = """
      $button-color: #CCCCCC;
      FooterButton {
        height: auto;
        width: auto;
        color: $button-color;
      }

    """

    def __init__(
        self,
        *,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=self.symbol, id=id, classes=classes, disabled=disabled)

    def render(self):
        return self

    def get_content_width(self, container, viewport) -> int:
        return len(self.name) + 2

    def get_content_height(self, container, viewport, width):
        return 1

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> Iterable[Segment]:
        segments = []
        style = self.get_component_rich_style()
        segments.append(Segment(f' {self.name} ', style=style))
        return segments


class Footer(Widget):

    DEFAULT_CSS = """
      Footer {
        dock: bottom;
        layout: horizontal;
        height: 1;
        width: 100%;
        background: #3b3b3b;
      }

    """

    def __init__(self, *buttons: list[FooterButton]):
        super().__init__()
        self.buttons = buttons

    def compose(self):
        for button in self.buttons:
            yield button
