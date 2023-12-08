from types import SimpleNamespace
import pygame
import xml.etree.ElementTree as ET
from pathlib import Path
from core.enums.log_level import LogLevel
from core.enums.sprite_type import SpriteType

from core.event_handler import EventHandler
from core.sprites.spritesheet import Spritesheet


class SpritesheetRepository:
    """Class for loading and handling spritesheets."""

    def __init__(self, root_path, spritesheets: list[tuple[SpriteType, str, int]]):
        self.root_path = Path(root_path)
        self.entries = {}

        self.create_entries(spritesheets)

        # private variables
        self._sprite_sheet = None
        self._mask_layers = None
        self._sprite_atlas = None

        # Create events
        self.events = SimpleNamespace()
        self.events.on_log_message = EventHandler()

    def create_entries(self, spritesheets: list[tuple[SpriteType, str, int]]):
        """Create spritesheet entries."""
        for sprite_type, file_name, mask_layer_amount in spritesheets:
            if sprite_type not in self.entries:
                self.entries[sprite_type] = []

            self.entries[sprite_type].append(
                Spritesheet(self.root_path / file_name, mask_layer_amount)
            )
    
    def get_spritesheets(self, sprite_type: SpriteType):
        """Returns a list of spritesheets for the given sprite type."""
        return self.entries[sprite_type]
    
    def get_all_spritesheets(self):
        """Returns a list of all spritesheets."""
        return [spritesheet for spritesheets in self.entries.values() for spritesheet in spritesheets]