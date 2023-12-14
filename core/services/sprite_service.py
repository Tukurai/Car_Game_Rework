from types import SimpleNamespace
from pathlib import Path
from injector import inject
from core.enums.log_level import LogLevel
from core.enums.sprite_type import SpriteType
from core.services.log_service import LogService
from core.services.service_base import ServiceBase
from core.sprites.sprite import Sprite
from core.sprites.spritesheet import Spritesheet
from core.sprites.spritesheet_repository import SpritesheetRepository
from settings import Settings


class SpriteService(ServiceBase):
    """Service for handling sprites."""

    @inject
    def __init__(self, log_service: LogService, settings: Settings):
        super().__init__(settings)
        self.services.logger = log_service
        self.spritesheet_root = Path(__file__).parents[2] / "assets" / "sprites"

        self.repository = SpritesheetRepository(
            self.spritesheet_root,
            [
                (SpriteType.VEHICLE, "spritesheet_vehicles.png", 1),
                (SpriteType.OBJECT, "spritesheet_objects.png", 1),
                (SpriteType.TILE, "spritesheet_tiles.png", 1),
                (SpriteType.UI, "greenSheet.png", 0),
                (SpriteType.UI, "blueSheet.png", 0),
                (SpriteType.UI, "redSheet.png", 0),
            ],
        )

        self.library = {}
        self.populate_library()

        # Add event handlers
        for spritesheet in self.repository.get_all_spritesheets():
            spritesheet.events.on_log_message += self.handle_log_message

    def get_sprite_from(self, type: SpriteType, key: str | int) -> Sprite:
        """Get a sprite from the library."""
        if isinstance(key, int):
            library = self.library[type].values()
            for sprite in library:
                if sprite.id == key:
                    return sprite.copy()
        else:
            return self.library[type][key].copy()

    def populate_library(self):
        """Populate the sprite library."""
        for type, spritesheet_list in self.repository.entries.items():
            for spritesheet in spritesheet_list:
                self.populate_library_type(type, spritesheet)

    def populate_library_type(self, type: SpriteType, spritesheet: Spritesheet):
        """Populate the sprite library for a specific type."""
        next_id = 0

        for name in spritesheet.get_sprite_atlas().keys():
            if type not in self.library:
                self.library[type] = {}
            else:
                next_id = list(self.library[type].values())[-1].id + 1

            self.library[type][name] = Sprite(
                spritesheet.get_sprite(name),
                spritesheet.get_mask_from_layer(name, 1),
                name,
                next_id,
                type,
                scale=Settings.SCALE[type],
            )

    def handle_log_message(self, message: str, log_level: LogLevel):
        """Handle a log message."""
        self.services.logger.log(message, log_level)
