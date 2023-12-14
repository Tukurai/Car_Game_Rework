import pygame
from core.components.component_base import ComponentBase
from core.enums.alignment import Alignment
from core.position import Position


class LabelComponent(ComponentBase):
    def __init__(
        self,
        name,
        position: Position,
        text,
        alignment: Alignment,
        font_size,
        font=None,
        color=(0, 0, 0),
        outline_color=(255, 255, 255),
        parent=None,
    ):
        super().__init__(name, position, alignment, parent)
        self.text = text
        self.font = font
        self.font_size = font_size
        self.color = color
        self.outline_color = outline_color

        self.font = pygame.font.Font(self.font, self.font_size)
        self.scaled_size = self.font.size(self.text)

    def handle_event(self, event):
        """This component does not handle events."""
        return

    def update(self, timedelta, input_state):
        """Update the component and all its children"""        
        self.scaled_size = self.font.size(self.text)

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children."""
        # Render the text with opacity, and center it
        rendered_text = self.font.render(self.text, True, (255, 255, 255, opacity))
        rendered_text.set_alpha(opacity)
        draw_x = self.position.get_pos()[0]
        draw_y = self.position.get_pos()[1]

        rendered_text_size = self.font.size(self.text)
        match self.alignment:
            case Alignment.LEFT:
                draw_y -= rendered_text_size[1] / 2.0
            case Alignment.CENTER:
                draw_x -= rendered_text_size[0] / 2.0
                draw_y -= rendered_text_size[1] / 2.0
            case Alignment.RIGHT:
                draw_x -= rendered_text_size[0]
                draw_y -= rendered_text_size[1] / 2.0

        # Draw the outline first
        rendered_text_outline = self.font.render(self.text, True, (0, 0, 0))
        rendered_text_outline.set_alpha(opacity)

        for x_offset in [-1, 1]:
            for y_offset in [-1, 1]:
                screen.blit(
                    rendered_text_outline, (draw_x + x_offset, draw_y + y_offset)
                )

        # Draw the text with opacity
        screen.blit(rendered_text, (draw_x, draw_y))

        super().draw(screen, opacity)  # Draw children after the background