import pygame
from core.components.component_base import ComponentBase
from core.position import Position


class ButtonComponent(ComponentBase):
    def __init__(
        self,
        name,
        position: Position,
        text: str,
        font,
        color,
        background: pygame.surface,
        hover: pygame.surface,
        active: pygame.surface,
        parent=None,
    ):
        super().__init__(name, position, parent)
        self.text = text
        self.font = font
        self.color = color
        self.sprite = background
        self.background = background
        self.hover = hover
        self.active = active
