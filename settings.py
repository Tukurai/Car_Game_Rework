from types import SimpleNamespace
from core.enums.sprite_type import SpriteType
from core.enums.log_level import LogLevel


class Settings:
    """The settings class, this is where all the settings are stored."""
    BASE_RESOLUTION = (1920, 1080)

    def __init__(self) -> None:
        self.resolution = (1920, 1080)
        self.fps = 60
        self.transition_speed = 1.0  # speed in seconds
        self.volume = SimpleNamespace(master=1.0, music=1.0, sfx=1.0)
        self.log_level = LogLevel.DEBUG
        self.tile_size = 128
        self.scale = {
            SpriteType.GLOBAL: 1.0, 
            SpriteType.OBJECT: 0.75, 
            SpriteType.TILE: 1.0, 
            SpriteType.VEHICLE: 0.5, 
            SpriteType.UI: 1.0,
        }

    def window_scale(self) -> tuple[float, float]:
        width_scale = self.resolution[0] / self.BASE_RESOLUTION[0]
        height_scale = self.resolution[1] / self.BASE_RESOLUTION[1]
        return (width_scale, height_scale)