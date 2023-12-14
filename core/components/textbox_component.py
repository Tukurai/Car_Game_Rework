from types import SimpleNamespace
import pygame
from core.components.component_base import ComponentBase
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.enums.log_level import LogLevel
from core.event_handler import EventHandler
from core.input_state import InputState
from core.position import Position
from core.relative import Relative


class TextboxComponent(ComponentBase):
    def __init__(
        self,
        name,
        position: Position,
        text: str,
        font_size: int,
        background: pygame.surface,
        hover: pygame.surface,
        active: pygame.surface,
        font=None,
        color=(0, 0, 0),
        outline_color=(255, 255, 255),
        alignment: Alignment = None,
        parent=None,
    ):
        super().__init__(name, position, alignment, parent)
        self.font = font
        self.font_size = font_size
        self.color = color
        self.outline_color = outline_color
        self.background_sprite = background
        self.hover_sprite = hover
        self.active_sprite = active

        self.background_sprite.position = Relative(self.position, (0, 0))
        self.hover_sprite.position = Relative(self.position, (0, 0))
        self.active_sprite.position = Relative(self.position, (0, 0))

        self.hover = False
        self.active = False

        self.scaled_size = self.background_sprite.get_scaled_size()

        self.label = LabelComponent(
            f"{self.name}_text",
            Relative(self.position, (self.scaled_size[0] / 2, self.scaled_size[1] / 2)),
            text,
            Alignment.CENTER,
            font_size,
            font,
            color,
            outline_color,
            self,
        )

        self.children.append(self.label)

        # Create events
        self.events = SimpleNamespace()
        self.events.on_textbox_focus = EventHandler()
        self.events.on_textbox_enter = EventHandler()
        self.events.on_log_message = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event, the button uses this to check for the pygame mouse events."""
        super().handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover is True:
                self.active = True
                self.events.on_textbox_focus.notify(self)
            else:
                self.active = False
                self.hover = False

        if event.type == pygame.KEYUP:
            if self.active:
                match event.key:
                    case pygame.K_RETURN:
                        self.events.on_textbox_enter.notify(self)
                        self.active = False
                    case pygame.K_BACKSPACE:
                        self.label.text = self.label.text[:-1]
                    case _:
                        if len(self.label.text) < 10 and event.unicode.isalnum():
                            self.label.text += event.unicode
                        else:
                            self.events.on_log_message.notify(
                                self, "You can only enter 10 alphanumeric characters", LogLevel.INFO
                            )

    def update(self, timedelta, input_state: InputState):
        """Update the component and all its children, the button uses this to check for the mouse hover."""
        if self.get_button_collision() is True:
            self.hover = True
        else:
            self.hover = False

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children, the button uses this to draw the background, children are drawn after the parent."""
        if self.active:
            self.active_sprite.draw(screen, opacity)
        elif self.hover:
            self.hover_sprite.draw(screen, opacity)
        else:
            self.background_sprite.draw(screen, opacity)

        super().draw(screen, opacity)  # Draw children after the background

    def get_button_collision(self):
        """Check if the mouse is colliding with the button."""
        return pygame.Rect(
            self.position.get_pos()[0],
            self.position.get_pos()[1],
            self.background_sprite.get_scaled_size()[0],
            self.background_sprite.get_scaled_size()[1],
        ).collidepoint(pygame.mouse.get_pos())

    def get_value(self):
        """Get the value of the textbox."""
        return self.label.text