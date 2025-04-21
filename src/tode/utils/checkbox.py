from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget


class Checkbox(Widget):
    #  󰄮 󰡖 󰄲 󰱒  󰄱 󰄵
    #  󰄱  󰄱 󰄱  󰄱 󰄵

    class Changed(Message):

        def __init__(self, value):
            self.value = value
            super().__init__()

    checked = reactive(False)

    def __init__(self, checked: bool = False):
        super().__init__()
        self.checked = checked

    def render(self):
        return "󰄲 " if self.checked else "󰄱 "

    def on_click(self, event):
        self.parent.post_message(Checkbox.Changed(not self.checked))
        self.post_message(Checkbox.Changed(not self.checked))

    def on_checkbox_changed(self, message) -> None:
        print(self, message)
        self.checked = message.value
