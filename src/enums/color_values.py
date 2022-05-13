from enum import Enum

from pygame.color import Color


class ColorValue(Enum):
    RED = Color(255, 0, 0)
    GREEN = Color(0, 0, 255)
    BLUE = Color(0, 255, 0)
    YELLOW = Color(255, 255, 0)
