from ast import Tuple
import copy
import pygame
from core.position import Position
from core.enums.sprite_type import SpriteType


class Sprite:
    def __init__(
        self,
        surface: pygame.Surface,
        mask: pygame.Surface,
        name: str,
        sprite_type: SpriteType,
        position: Position = Position((0, 0)),
        rotation: float = 0,
        scale: float = 1.0,
        opacity: int = 255,
    ):
        self.surface = surface
        self.mask = mask
        self.name = name
        self.sprite_type = sprite_type

        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.opacity = opacity

    def draw(self, screen: pygame.Surface, opacity: int = 255):
        self.opacity = opacity

        sprite, offset = self.get_sprite()
        screen.blit(sprite, self.position + offset)

    def copy(self):
        return copy.copy(self)

    def get_scaled_size(self) -> tuple[int, int]:
        """Returns the scaled height of the object"""
        return (
            int(self.surface.get_width() * self.scale),
            int(self.surface.get_height() * self.scale),
        )

    def get_mask(self) -> tuple[pygame.Surface | None, Position]:
        """Returns a scaled, rotated surface, and mask, also return the center offset as a Position"""
        mask, offset = self.__get_transformed_surface(self.mask)
        return (mask, offset)
    
    def get_sprite(self) -> tuple[pygame.Surface, Position]:
        """Returns a scaled, rotated surface, and mask with opacity, also return the center offset as a Position"""
        sprite, offset = self.__get_transformed_surface(self.surface)
        return (sprite, offset)

    def __get_transformed_surface(self, surface) -> tuple[pygame.Surface, Position]:
        """Returns a scaled, rotated surface with opacity, also return the center offset as a Position"""
        surface = pygame.transform.scale(surface, self.get_scaled_size())

        center_offset = Position((0, 0))
        if self.rotation is not None:
            # Create a new surface with the image, rotated
            surface = pygame.transform.rotate(surface, -self.rotation)
            # Calculate the new upper left corner position of the rotated car
            rect = surface.get_rect()
            original_rect = surface.get_rect(topleft=(self.position.x, self.position.y))

            center_offset.x = original_rect.centerx - rect.centerx
            center_offset.y = original_rect.centery - rect.centery

        surface = surface.convert_alpha()
        surface.set_alpha(self.opacity)

        return (surface, center_offset)
