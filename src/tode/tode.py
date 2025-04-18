"""Main module."""
# cSpell:disable

from textual.app import App
from window_manager.window import Window
# from window_manager.panel import Panel
from textual.widgets import Static
from textual.widget import Widget

# from apps.border_editor import BorderEditor
from apps.image_editor import ImageEditor


class Tode(App):
    CSS_PATH = "css/tode.tcss"

    def create_window(self, content: Widget):
        window = Window(content)
        self.push_screen(window)
        self.windows.append(window)

    def on_mount(self):
        self.windows = []
        self.create_window(ImageEditor())

    def compose(self):
        yield Static("hi")


if __name__ == "__main__":
    Tode().run()
