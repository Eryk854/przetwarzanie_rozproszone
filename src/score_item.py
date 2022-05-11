from typing import Tuple


class ScoreItem:
    def __init__(self, x: int, y: int, radius: int, color: Tuple[int, int, int], score_value: int) -> None:
        self.x: int = x
        self.y: int = y
        self.radius: int = radius
        self.color: Tuple[int, int, int] = color
        self.score_value: int = score_value

        self.coordinates: Tuple[int, int] = (self.x, self.y)
