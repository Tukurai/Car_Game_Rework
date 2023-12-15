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
        id: int,
        sprite_type: SpriteType,
        position: Position = Position((0, 0)),
        rotation: float = None,
        scale: float = 1.0,
        opacity: int = 255,
    ):
        self.surface = surface
        self.mask = mask
        self.name = name
        self.id = id
        self.sprite_type = sprite_type

        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.opacity = opacity

        self.__scaled_surface = None
        self.__scaled_mask = None

    def draw(self, screen: pygame.Surface, opacity: int = 255):
        self.opacity = opacity

        sprite, offset = self.get_sprite()
        if self.mask is not None:
            sprite, offset = self.get_mask()

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
        if self.__scaled_mask is None:
            self.__scaled_mask = pygame.transform.scale(self.mask, self.get_scaled_size())
        mask = self.__scaled_mask

        mask, offset = self.__get_transformed_surface(mask, False)
        return (mask, offset)
    
    def get_sprite(self) -> tuple[pygame.Surface, Position]:
        """Returns a scaled, rotated surface, and mask with opacity, also return the center offset as a Position"""
        if self.__scaled_surface is None:
            self.__scaled_surface = pygame.transform.scale(self.surface, self.get_scaled_size())
        surface = self.__scaled_surface

        sprite, offset = self.__get_transformed_surface(surface, True)
        return (sprite, offset)

    def __get_transformed_surface(self, surface, has_opacity) -> tuple[pygame.Surface, Position]:
        """Returns a scaled, rotated surface with opacity, also return the center offset as a Position"""
        center_offset = Position((0, 0))
        if self.rotation is not None:
            # Create a new surface with the image, rotated
            old_center = surface.get_rect().center
            surface = pygame.transform.rotate(surface, -self.rotation)
            rect = surface.get_rect()
            rect.center = old_center

            center_offset = Position((-(surface.get_width() / 2), -(surface.get_height() / 2)))

        if has_opacity:
            surface = surface.convert_alpha()
            surface.set_alpha(self.opacity)

        return (surface, center_offset)
