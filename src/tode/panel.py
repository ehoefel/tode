from textual.screen import ModalScreen
from textual.widgets import Placeholder
from textual.containers import Grid


class Panel(ModalScreen):

    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def compose(self):
        yield self.widget
