from enum import Enum


class SizeState(str, Enum):
    minimized = "minimized"
    maximized = "maximized"
    restored = "restored"
    fullscreen = "fullscreen"
