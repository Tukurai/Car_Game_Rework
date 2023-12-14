import pygame


class Helper:
    @staticmethod
    def get_middle_positions(width, segments) -> list:
        """Get the middle positions of the given amount of segments."""

        segment_width = width / segments
        middle_positions = []
        for i in range(segments):
            segment_start = i * segment_width
            middle_position = segment_start + (segment_width / 2)
            middle_positions.append(middle_position)
        return middle_positions

    @staticmethod
    def draw_outline(
        screen: pygame.surface,
        position: tuple[int, int],
        scaled_size: tuple[int, int],
        color,
        thickness,
        opacity: int = 255,
    ):
        rect = pygame.Rect(
            position[0] - (thickness * 2),
            position[1] - (thickness * 2),
            scaled_size[0] + (thickness * 4),
            scaled_size[1] + (thickness * 4),
        )
        pygame.draw.rect(screen, color, rect, thickness)
