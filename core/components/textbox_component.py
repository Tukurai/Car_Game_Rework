import pygame
from core.components.component_base import ComponentBase
from core.position import Position


class TextboxComponent(ComponentBase):
    def __init__(
        self,
        name,
        position: Position,
        value: str,
        font,
        color,
        background: pygame.surface,
        hover: pygame.surface,
        active: pygame.surface,
        parent=None,
    ):
        super().__init__(name, position, parent)
        self.value = value
        self.font = font
        self.color = color
        self.sprite = background
        self.background = background
        self.hover = hover
        self.active = active
