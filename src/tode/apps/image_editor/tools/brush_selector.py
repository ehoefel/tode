# cSpell:disable
import colorsys

from typing import Iterable

from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions
from rich.segment import Segment
from rich.style import Style

from textual.color import Color
from textual.message import Message
from textual.reactive import reactive
from textual.strip import Strip
from textual.widget import Widget
from textual.widgets import Static, Input


class BrushSelected(Message):

    def __init__(self, brush: str | None) -> None:
        super().__init__()
        self.brush = brush


class BrushSelector(Widget):

    DEFAULT_CSS = """
     BrushSelector {
        height: auto;
        padding: 0 1;
        Input, Input:hover, Input:focus {
          height: 1;
          width: 100%;
          border: none;
          text-align: left;
          padding: 0;

          .input--placeholder {
            text-style: italic;
          }
        }
     }

    """

    selected = reactive(None)

    def __init__(self, selected: str | None = None) -> None:
        super().__init__()
        self.selected = selected

    def compose(self):
        yield Input(placeholder="filter", select_on_focus=False)
