from types import SimpleNamespace
import pygame
import xml.etree.ElementTree as ET
from pathlib import Path
from core.enums.log_level import LogLevel

from core.event_handler import EventHandler


class Spritesheet:
    """Class for loading and handling spritesheets."""

    def __init__(self, file_path, mask_layer_amount: int = 0):
        self.file_path = Path(file_path)
        self.mask_layer_amount = mask_layer_amount

        # private variables
        self._sprite_sheet = None
        self._mask_layers = None
        self._sprite_atlas = None

        # Create events
        self.events = SimpleNamespace()
        self.events.on_log_message = EventHandler()

    def get_sprite_atlas(self):
        """Returns a dictionary with the sprite atlas, loads the atlas if it hasn't been loaded."""
        if self._sprite_atlas is None:
            self._sprite_atlas = self.load_atlas()
        return self._sprite_atlas

    def get_sprite_sheet(self):
        """Returns the sprite sheet, loads the image if it hasn't been loaded."""
        if self._sprite_sheet is None:
            self._sprite_sheet = self.load_image(self.file_path)
        return self._sprite_sheet

    def get_mask_layers(self):
        """Returns a dictionary with the mask layers, loads the images if they haven't been loaded."""
        if self._mask_layers is None:
            self._mask_layers = {
                layer: self.load_image(
                    self.file_path.with_stem(f"{self.file_path.stem}_mask{layer}")
                )
                for layer in range(self.mask_layer_amount)
            }

    def load_image(self, file_path: Path):
        """Loads an image from a file path."""
        self.events.on_log_message.notify(
            f"Loading [Spritesheet]:  {file_path}", LogLevel.DEBUG
        )
        return pygame.image.load(str(file_path)).convert()

    def load_atlas(self):
        """Loads the sprite atlas from a file path, based on the file name for this sprite sheet."""
        tree = ET.parse(str(self.file_path.with_suffix(".xml")))
        root = tree.getroot()
        return {
            subtexture.get("name"): {
                "x": int(subtexture.get("x")),
                "y": int(subtexture.get("y")),
                "w": int(subtexture.get("width")),
                "h": int(subtexture.get("height")),
            }
            for subtexture in root.findall("SubTexture")
        }

    def create_sprite_from_sheet(
        self, x: int, y: int, w: int, h: int, sheet: pygame.Surface
    ):
        """Create a sprite from a sheet, coordinates usually come from the sprite sheet its xml."""
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(sheet, (0, 0), (x, y, w, h))
        return sprite

    def get_sprite(self, name: str):
        """Get a sprite from the sprite sheet."""
        x, y, w, h = self.get_sprite_atlas()[name].values()
        return self.create_sprite_from_sheet(x, y, w, h, self.get_sprite_sheet())

    def get_mask_from_layer(self, name: str, mask_layer: int):
        """Get a mask from a layer of the sprite sheet."""
        if self.mask_layer_amount == 0 or mask_layer >= self.mask_layer_amount:
            return None

        x, y, w, h = self.get_sprite_atlas()[name].values()
        return self.create_sprite_from_sheet(
            x, y, w, h, self.get_mask_layers()[mask_layer]
        )

    def get_mask_from_all_layers(self, name: str):
        """Get a mask from all layers of the sprite sheet."""
        return {
            layer: self.get_mask_from_layer(name, layer)
            for layer in self.get_mask_layers()
        }
