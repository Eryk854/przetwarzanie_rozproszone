from typing import Tuple

import pygame

from read_config_value import read_config_value

SCREEN_WIDTH = read_config_value("screen_width")
SCREEN_HEIGHT = read_config_value("screen_height")


class Player:
    def __init__(self, x: int, y: int, width: int, height: int, color: Tuple[int, int, int]) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.color: Tuple[int, int, int] = color
        self.rect: Tuple[int, int, int, int] = (x, y, width, height)
        self.vel: int = 3
        self.points: int = 0
        self.rect_obj: pygame.Rect = pygame.Rect(self.rect)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
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

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
        self.rect_obj = pygame.Rect(self.rect)
