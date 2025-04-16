"""Main module."""
# cSpell:disable

from textual.app import App
from window import Window
from panel import Panel
from textual.widgets import Static
from border_style import BorderStyle
from border_editor import BorderEditor


class Tode(App):
    CSS_PATH = "css/tode.tcss"

    def __init__(self):
        super().__init__()
        self.windows = []
        self.set_border_style(BorderStyle())

    def create_window(self, content=None):
        window = Window(size=self.size)
        window.decorator.set_border_style(self.border_style)
        self.push_screen(window)
        self.windows.append(window)

    def on_resize(self, event):
        for window in self.windows:
            window.on_app_resize(event)

    def on_mount(self):
        style = BorderStyle(bottom=".")
        self.set_border_style(style)

        self.create_window()
        self.push_screen(Panel(BorderEditor()))

    def compose(self):
        yield Static("hi")

    def set_border_style(self, style):
        self.border_style = style
        for window in self.windows:
            window.decorator.set_border_style(style)


if __name__ == "__main__":
    Tode().run()
