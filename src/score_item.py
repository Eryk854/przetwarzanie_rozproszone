from typing import Tuple

from pygame import Color


class ScoreItem:
    def __init__(self, x: int, y: int, radius: int, color: Color, score_value: int) -> None:
        self.x: int = x
        self.y: int = y
        self.radius: int = radius
        self.color: Color = color
        self.score_value: int = score_value

        self.coordinates: Tuple[int, int] = (self.x, self.y)
