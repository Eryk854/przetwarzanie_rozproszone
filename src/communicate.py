from typing import Tuple


class Communicate:
    def __init__(
        self,
        text: str,
        color: Tuple[int, int, int],
        font_size: int,
        coordinates: Tuple[int, int],
        font_name: str = "comicsans",
        antialias: bool = True
    ) -> None:
        self.text: str = text
        self.color: Tuple[int, int, int] = color
        self.font_size: int = font_size
        self.coordinates: Tuple[int, int] = coordinates
        self.font_name: str = font_name
        self.antialias = antialias
