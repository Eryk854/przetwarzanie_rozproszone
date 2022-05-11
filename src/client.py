import pickle
import random
import socket
import time
from threading import Thread
from typing import List

import pygame

from src.player import Player
from src.score_item import ScoreItem

pygame.font.init()

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.240.1"
ADDR = (SERVER, PORT)

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)

import math


def collision(rleft, rtop, width, height,   # rectangle definition
              center_x, center_y, radius):  # circle definition
    """ Detect collision between a rectangle and circle. """

    # complete boundbox of the rectangle
    rright, rbottom = rleft + width/2, rtop + height/2

    # bounding box of the circle
    cleft, ctop     = center_x-radius, center_y-radius
    cright, cbottom = center_x+radius, center_y+radius

    # trivial reject if bounding boxes do not intersect
    if rright < cleft or rleft > cright or rbottom < ctop or rtop > cbottom:
        return False  # no collision possible

    # check whether any point of rectangle is inside circle's radius
    for x in (rleft, rleft+width):
        for y in (rtop, rtop+height):
            # compare distance between circle's center point and each point of
            # the rectangle with the circle's radius
            if math.hypot(x-center_x, y-center_y) <= radius:
                return True  # collision detected

    # check if center of circle is inside rectangle
    if rleft <= center_x <= rright and rtop <= center_y <= rbottom:
        return True  # overlaid

    return False  # no collision detected


def generate_score_item() -> ScoreItem:
    x = random.randint(0, width)
    y = random.randint(0, height)
    radius = random.randrange(5, 20, 5)
    score_value = 25 - radius
    color = (150, 105, 150)
    return ScoreItem(x, y, radius, color, score_value)


def generate_score_items(elements: int = 10) -> List[ScoreItem]:
    score_items = []
    for _ in range(elements):
        score_item = generate_score_item()
        score_items.append(score_item)
    return score_items


def add_new_score_items(score_items: List[ScoreItem]) -> None:
    sleep_time = 5
    while True:
        score_item = generate_score_item()
        score_items.append(score_item)
        time.sleep(sleep_time)


def check_score_item_collision(score_items: List[ScoreItem], player: Player) -> None:
    for idx, score_item in enumerate(score_items):
        collision_flag = collision(
            player.x,
            player.y,
            player.width,
            player.height,
            score_item.x,
            score_item.y,
            score_item.radius
        )
        if collision_flag:
            del score_items[idx]
            player.points += score_item.score_value


def redrawWindow(win, player: Player, score_items: List[ScoreItem]) -> None:
    win.fill((255, 255, 255))
    player.draw(win)
    for score_item in score_items:
        pygame.draw.circle(
            surface=win,
            color=score_item.color,
            center=score_item.coordinates,
            radius=score_item.radius
        )

    font = pygame.font.SysFont(name="comicsans", size=24)
    img = font.render(f"Your result: {player.points}", True, (255, 255, 0), None)
    win.blit(img, (0, width-50))

    pygame.display.update()


def send(player: Player):
    client.send(pickle.dumps(player))


def main():
    run = True
    p = Player(x=0, y=0, width=25, height=25, color=(0, 255, 255))
    score_items = generate_score_items()
    clock = pygame.time.Clock()
    score_items_thread = Thread(target=add_new_score_items, args=(score_items,), daemon=True)
    score_items_thread.start()
    while run:
        clock.tick(120)
        check_score_item_collision(score_items, p)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, score_items)

main()
