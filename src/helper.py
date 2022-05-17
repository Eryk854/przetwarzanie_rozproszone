from pygame.rect import Rect

from configuration.read_config_value import read_config_value


def get_town() -> Rect:
    town_width = read_config_value("town_width")
    town_height = read_config_value("town_height")
    width = read_config_value("screen_width")
    height = read_config_value("screen_height")
    town = Rect(0, 0, town_width, town_height)
    town.center = (width // 2, height // 2)
    return town
