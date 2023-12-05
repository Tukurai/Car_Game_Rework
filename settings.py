from types import SimpleNamespace


class Settings():
    def __init__(self) -> None:
        self.resolution = (800, 600)
        self.fps = 60
        self.volume = SimpleNamespace(master=1.0, music=1.0, sfx=1.0)