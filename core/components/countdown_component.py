from types import SimpleNamespace
import pygame
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.event_handler import EventHandler
from core.position import Position


class CountdownComponent(LabelComponent):
    def __init__(
        self,
        name,
        position: Position,
        texts_timeouts: list[tuple[str, float]],
        alignment: Alignment,
        font_size,
        font=None,
        color=(0, 0, 0),
        outline_color=(255, 255, 255),
        parent=None,
    ):
        super().__init__(
            name, position, "", alignment, font_size, font, color, outline_color, parent
        )
        self.text = texts_timeouts[0][0]
        self.timeout = texts_timeouts[0][1]
        self.texts_timeouts = texts_timeouts
        self.active = False
        self.text_index = 0

        # events
        self.events = SimpleNamespace()
        self.events.on_timeout_complete = EventHandler()

    def handle_event(self, event):
        """This component does not handle events."""
        return

    def update(self, timedelta, input_state):
        """Update the component and all its children"""
        if self.timeout > -1:
            self.timeout -= timedelta
            if self.timeout <= 0:
                self.step()

        super().update(timedelta, input_state)

    def step(self):
        self.text_index += 1
        self.active = True
        if self.text_index >= len(self.texts_timeouts):
            self.text = ""
            self.timeout = -1
            self.active = False
            self.events.on_timeout_complete.notify(self)
        else:
            self.text = self.texts_timeouts[self.text_index][0]
            self.timeout = self.texts_timeouts[self.text_index][1]
            if self.timeout == -1:
                self.active = False
                self.events.on_timeout_complete.notify(self)

