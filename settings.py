from types import SimpleNamespace

from core.enums.log_level import LogLevel


class Settings():
    def __init__(self) -> None:
        self.resolution = (800, 600)
        self.fps = 60
        self.transition_speed = 1.0 # speed in seconds
        self.volume = SimpleNamespace(master=1.0, music=1.0, sfx=1.0)
        self.log_level = LogLevel.DEBUG