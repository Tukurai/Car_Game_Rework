from pygame import key
import pygame


class InputState:
    """A class to represent the input state of the game."""

    def __init__(self):
        self.update()

    def update(self):
        """Update the input state."""
        self.prev_keyboard_state = self.cur_keyboard_state
        self.prev_mouse_state = self.cur_mouse_state
        self.cur_keyboard_state = pygame.key.get_pressed()
        self.cur_mouse_state = pygame.mouse.get_pressed()
