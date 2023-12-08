from core.components.component_base import ComponentBase
from core.position import Position


class LabelComponent(ComponentBase):
    def __init__(
        self, name, position: Position, text, font, color, outline_color, parent=None
    ):
        super().__init__(name, position, parent)
        self.text = text
        self.font = font
        self.color = color
        self.outline_color = outline_color
