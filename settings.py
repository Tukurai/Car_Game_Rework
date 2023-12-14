from types import SimpleNamespace
from core.car_properties import CarProperties
from core.enums.sprite_type import SpriteType
from core.enums.log_level import LogLevel


class Settings:
    """The settings class, this is where all the settings are stored."""

    BASE_RESOLUTION = (1920, 1080)
    MAP_OFFSET = 64
    TILE_SIZE = 128
    MAX_PLAYERS = 4
    TRANSITION_SPEED = 1  # speed in seconds
    SCALE = {
        SpriteType.GLOBAL: 1.0,
        SpriteType.OBJECT: 0.75,
        SpriteType.TILE: 1.0,
        SpriteType.VEHICLE: 0.5,
        SpriteType.UI: 1.0,
    }
    CAR_OPTIONS = car_options = [
        ("Black", "car_black_small_1.png", CarProperties(180, 2, 3, 1.0, 30, 6)),
        ("Red", "car_red_small_1.png", CarProperties(240, 2, 3, 1.0, 25, 6)),
        ("Yellow", "car_yellow_small_1.png", CarProperties(220, 2, 3, 1.0, 27, 6)),
        ("Green", "car_green_small_1.png", CarProperties(160, 2, 3, 1.0, 35, 6)),
        ("Blue", "car_blue_small_1.png", CarProperties(280, 2, 3, 1.0, 20, 6)),
    ]
    LOG_LEVEL = LogLevel.DEBUG
    FPS = 60

    def __init__(self) -> None:
        self.resolution = (1920, 1080)
        self.volume = SimpleNamespace(master=1.0, music=1.0, sfx=1.0)

    def window_scale(self) -> tuple[float, float]:
        width_scale = self.resolution[0] / self.BASE_RESOLUTION[0]
        height_scale = self.resolution[1] / self.BASE_RESOLUTION[1]
        return (width_scale, height_scale)
