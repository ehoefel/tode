from textual.widget import Widget
from textual.widgets import Static, Placeholder, Rule, TabbedContent
from textual.containers import Grid
from textual.reactive import reactive
from textual.message import Message


from window_manager.border import VerticalBorderRenderable
from window_manager.border_style import BorderStyle

PALETTE = """
▉▕█▘▙▚▝▞▟
▊🮇▁▂▃▄▅▆▇
▋🮈▔🮂🮃▀🮄🮅🮆
▌▐🮑🮑
▍🮉🭁🭃⌝
▎🮊🬼🬾🭏
▏🮋
"""


class PropSelected(Message):

    def __init__(self, prop_name: str) -> None:
        super().__init__()
        self.prop_name = prop_name


class ValueSelected(Message):

    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value


class PropValueChange(Message):

    def __init__(self, prop_name: str, value: str) -> None:
        super().__init__()
        self.prop_name = prop_name
        self.value = value


class PropSelector(Widget):

    border_style = reactive(None)

    def __init__(
        self,
        prop_name: str,
        style: BorderStyle | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.prop_name = prop_name
        self.border_style = style

    def render(self):
        value = getattr(self.border_style, self.prop_name)
        if self.content_size.width > 1:
            return value * self.content_size.width
        if self.content_size.height > 1:
            height = self.content_size.height
            return VerticalBorderRenderable(value, None, height)

        return value

    def on_click(self):
        self.post_message(PropSelected(self.prop_name))


class Preview(Grid):

    border_style = reactive(None)

    def __init__(
        self,
        style: BorderStyle | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.border_style = style

    def highlight_prop(self, prop_name):
        for child in self.children:
            if child.id == prop_name:
                child.add_class("-highlighted")
            else:
                child.remove_class("-highlighted")

    def watch_border_style(self, old_values, new_values) -> None:
        for child in self.children:
            if type(child) == PropSelector:
                child.border_style = new_values


    def compose(self):
        props = ["top_left", "top", "top_right",
                 "left", None, "right",
                 "bottom_left", "bottom", "bottom_right"]
        for prop in props:
            if prop is None:
                yield Placeholder("preview", id="preview")
            else:
                yield PropSelector(prop, self.border_style, id=prop)


class Palette(Grid):

    selected_option = reactive(None, recompose=True)
    _options = []

    class PaletteOption(Static):

        def __init__(self, value):
            super().__init__(value)
            self.value = value

        def on_click(self, event):
            self.post_message(ValueSelected(self.value))

    def __init__(
        self,
        options: str,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.options = options.strip()

    def compose(self):
        columns = 0
        matrix = []
        for line in self.options.strip().split("\n"):
            row = []
            for cell in line:
                row.append(Palette.PaletteOption(cell))
            matrix.append(row)
            columns = max(columns, len(line))
        for row in matrix:
            if len(row) < columns:
                row[-1].styles.column_span = columns - len(row) + 1
            for cell in row:
                yield cell

        self.styles.grid_size_columns = columns


class PropEditor(Widget):

    selected_prop = reactive(None, recompose=True)
    border_style = reactive(None, recompose=True)

    def __init__(
        self,
        style: BorderStyle | None = None,
        *,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.border_style = style
        self.select_prop(self.selected_prop)
        self.palette = Palette(PALETTE)

    def select_prop(self, prop_name):
        def prop_to_str(prop):
            if prop is None:
                return "none"
            return prop

        self.remove_class(f"-{prop_to_str(self.selected_prop)}")
        self.selected_prop = prop_name
        self.add_class(f"-{prop_to_str(self.selected_prop)}")

    def compose(self):
        if self.selected_prop is None:
            yield Static("Select a property")
            return

        title = self.selected_prop

        with TabbedContent("󰗈", "󰢵", "󱍜"):
            yield self.palette
            yield Placeholder("under construction")
            yield Placeholder("under construction")

    def on_value_selected(self, event):
        event.stop()
        self.post_message(PropValueChange(self.selected_prop, event.value))


class BorderEditor(Widget):

    border_style = reactive(BorderStyle())
    values = {}

    def __init__(self):
        super().__init__()

    def watch_border_style(self, old_values, new_values) -> None:
        if not self.is_mounted:
            return
        self.get_child_by_type(Preview).border_style = new_values
        self.get_child_by_type(PropEditor).border_style = new_values

    def on_prop_selected(self, event):
        event.stop()
        self.get_child_by_type(Preview).highlight_prop(event.prop_name)
        self.get_child_by_type(PropEditor).select_prop(event.prop_name)

    def compose(self):
        yield Static("Border Editor", classes="title")
        yield Preview(self.border_style)
        yield Rule()
        yield PropEditor(self.border_style)

    def get_content_width(self, container, viewport) -> int:
        return max(30, container.width / 5)

    def on_prop_value_change(self, event):
        event.stop()
        self.values[event.prop_name] = event.value
        self.border_style = BorderStyle(**self.values)
