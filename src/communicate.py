from typing import Tuple, List

import pygame
from pygame import display
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

    def render_communicate(self, win, clear_display: bool = False, update: bool = True):
        if clear_display:
            win.fill(Color(255, 255, 255))
        font = pygame.font.SysFont(self.font_name, self.font_size)
        text = font.render(self.text, self.antialias, self.color)
        win.blit(text, self.coordinates)
        if update:
            display.update()

    @classmethod
    def render_multiple_communicates(cls, communicates: List["Communicate"], win):
        win.fill(Color(255, 255, 255))
        for communicate in communicates:
            communicate.render_communicate(win, False, False)
        display.update()
