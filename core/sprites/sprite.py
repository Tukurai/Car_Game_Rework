import copy
import pygame
from core.position import Position
from core.enums.sprite_type import SpriteType
from settings import Settings


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
        self.__scaled_surface = None
        self.__transformed_surface = None
        self.__transformed_surface_offset = None
        self.__last_surface_rotation = None
        self.__last_surface_opacity = None
        self.mask_surface = mask
        self.__scaled_mask_surface = None
        self.__transformed_mask_surface = None
        self.__transformed_mask_surface_offset = None
        self.__last_mask_surface_rotation = None
        self.__mask = None
        self.name = name
        self.id = id
        self.sprite_type = sprite_type

        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.opacity = opacity

    def draw(self, screen: pygame.Surface, opacity: int = 255):
        self.opacity = opacity

        sprite, offset = self.get_sprite()
        screen.blit(sprite, self.position.get_absolute_pos() + offset)
        
        if Settings.DRAW_MASKS and self.mask_surface is not None:
            _, offset, sprite_mask = self.get_mask()
            screen.blit(sprite_mask, self.position.get_absolute_pos() + offset)


    def copy(self):
        return copy.copy(self)

    def get_scaled_size(self) -> tuple[int, int]:
        """Returns the scaled height of the object"""
        return (
            int(self.surface.get_width() * self.scale),
            int(self.surface.get_height() * self.scale),
        )

    def get_mask(self) -> tuple[pygame.mask.Mask | None, Position, pygame.Surface]:
        """Returns a scaled, rotated surface, and mask, also return the center offset as a Position"""
        if self.__scaled_mask_surface is None:
            self.__scaled_mask_surface = pygame.transform.scale(
                self.mask_surface, self.get_scaled_size()
            )

        if (
            self.rotation != self.__last_mask_surface_rotation
            or self.__mask is None
            or self.__transformed_mask_surface is None
        ):
            (
                self.__transformed_mask_surface,
                self.__transformed_mask_surface_offset,
            ) = self.__get_transformed_surface(self.__scaled_mask_surface, False)
            self.__mask = pygame.mask.from_surface(self.__scaled_mask_surface)
            self.__last_mask_surface_rotation = self.rotation

        return (
            self.__mask,
            self.__transformed_mask_surface_offset,
            self.__transformed_mask_surface,
        )

    def get_sprite(self) -> tuple[pygame.Surface, Position]:
        """Returns a scaled, rotated surface, and mask with opacity, also return the center offset as a Position"""
        if self.__scaled_surface is None:
            self.__scaled_surface = pygame.transform.scale(
                self.surface, self.get_scaled_size()
            )

        if (
            self.rotation != self.__last_surface_rotation
            or self.opacity != self.__last_surface_opacity
            or self.__transformed_surface is None
        ):
            (
                self.__transformed_surface,
                self.__transformed_surface_offset,
            ) = self.__get_transformed_surface(self.__scaled_surface, True)
            self.__last_surface_rotation = self.rotation
            self.__last_surface_opacity = self.opacity

        return (self.__transformed_surface, self.__transformed_surface_offset)

    def __get_transformed_surface(
        self, surface, has_opacity
    ) -> tuple[pygame.Surface, Position]:
        """Returns a scaled, rotated surface with opacity, also return the center offset as a Position"""
        center_offset = Position((0, 0))
        if self.rotation is not None:
            # Create a new surface with the image, rotated
            old_center = surface.get_rect().center
            surface = pygame.transform.rotate(surface, -self.rotation)
            rect = surface.get_rect()
            rect.center = old_center

            center_offset = Position(
                (-(surface.get_width() / 2), -(surface.get_height() / 2))
            )

        if has_opacity:
            surface = surface.convert_alpha()
            surface.set_alpha(self.opacity)

        return (surface, center_offset)
