from typing import Tuple

import pygame
from pygame.color import Color
from pygame.surface import Surface

from configuration.read_config_value import read_config_value

SCREEN_WIDTH = read_config_value("screen_width")
SCREEN_HEIGHT = read_config_value("screen_height")


class Player:
    def __init__(self, x: int, y: int, width: int, height: int, color: Color) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.color: Color = color
        self.rect: Tuple[int, int, int, int] = (x, y, width, height)
        self.vel: int = 3
        self.points: int = 0
        self.rect_obj: pygame.Rect = pygame.Rect(self.rect)
        self.fight: bool = False

    def draw(self, win: Surface) -> None:
        pygame.draw.rect(win, self.color, self.rect)

    def move(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        if self.x <= 0:
            self.x = 0
        if self.x + self.width >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        if self.y <= 0:
            self.y = 0
        if self.y + self.height - self.vel >= SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height

        self.update()

    def update(self) -> None:
        self.rect = (self.x, self.y, self.width, self.height)
        self.rect_obj = pygame.Rect(self.rect)

    def fight_result_points(self, winner: bool) -> None:
        if winner:
            self.points += 100
        else:
            self.points -= 100
            if self.points < 0:
                self.points = 0
