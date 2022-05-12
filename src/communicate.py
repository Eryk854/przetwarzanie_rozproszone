from typing import Tuple

from pygame.color import Color


class Communicate:
    def __init__(
        self,
        text: str,
        color: Color,
        font_size: int,
        coordinates: Tuple[int, int],
        font_name: str = "comicsans",
        antialias: bool = True
    ) -> None:
        self.text: str = text
        self.color: Color = color
        self.font_size: int = font_size
        self.coordinates: Tuple[int, int] = coordinates
        self.font_name: str = font_name
        self.antialias = antialias
