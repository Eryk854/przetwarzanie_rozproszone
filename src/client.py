import pickle
import random
import socket
import time
from threading import Thread
from typing import List, Tuple

import pygame

from communicate import Communicate
from read_config_value import read_config_value
from src.player import Player
from src.score_item import ScoreItem

pygame.font.init()

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.240.1"
ADDR = (SERVER, PORT)

WIDTH = read_config_value("screen_width")
HEIGHT = read_config_value("screen_height")
win = pygame.display.set_mode((WIDTH, HEIGHT))
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
    radius = random.randrange(5, 20, 5)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    while (x + radius >= WIDTH) or (x - radius <= 0):
        x = random.randint(0, WIDTH)
    while (y + radius >= HEIGHT) or (y - radius <= 0):
        y = random.randint(0, HEIGHT)

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


def generate_player_starting_point(
        area: pygame.Rect, player_width: int, player_height: int
) -> Tuple[int, int]:
    x = random.randint(area.left, area.right - player_width)
    y = random.randint(area.top, area.bottom - player_height)
    return x, y


def redrawWindow(win, player: Player, player2: Player, score_items: List[ScoreItem], town: pygame.Rect) -> None:
    win.fill((255, 255, 255))
    pygame.draw.rect(win, (200, 200, 200), town)
    player.draw(win)
    player2.draw(win)

    for score_item in score_items:
        pygame.draw.circle(
            surface=win,
            color=score_item.color,
            center=score_item.coordinates,
            radius=score_item.radius
        )

    font = pygame.font.SysFont(name="comicsans", size=24)
    img = font.render(f"Your result: {player.points}", True, (255, 255, 0), None)
    win.blit(img, (0, WIDTH-50))



    pygame.display.update()


def send(player: Player):
     client.send(pickle.dumps(player))


def render_texts(communicates: List[Communicate]) -> None:
    win.fill((255, 255, 255))
    for communicate in communicates:
        font = pygame.font.SysFont(communicate.font_name, communicate.font_size)
        text = font.render(communicate.text, communicate.antialias, communicate.color)
        win.blit(text, communicate.coordinates)
    pygame.display.update()


def fight_screen():
    fight_init_communicate = Communicate(
        text="Fight screen! Press Enter button to win",
        color=(255, 0, 0),
        font_size=42,
        coordinates=(100, 200)
    )

    render_texts([fight_init_communicate])
    start_ticks = pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        fight_count_communicate = Communicate(
            text=f"Fight starts in {round(5 - seconds, 2)}",
            color=(255, 0, 0),
            font_size=42,
            coordinates=(100, 400)
        )
        render_texts([fight_init_communicate, fight_count_communicate])
        if seconds > 5:
            break
    start_fight_communicate = Communicate(
        text=f"Start fight! Press Enter button to win",
        color=(255, 0, 0),
        font_size=42,
        coordinates=(100, 400)
    )
    render_texts([start_fight_communicate])
    timeout = time.time() + 5
    count = 0
    while time.time() < timeout:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    count += 1
                    fight_count_communicate = Communicate(
                        text=f"You press Enter: {count} times",
                        color=(255, 0, 0),
                        font_size=42,
                        coordinates=(100, 400)
                    )
                    render_texts([fight_init_communicate, fight_count_communicate])

    if count > 20:
        text = "You won!!"
    else:
        text = "You lose :("
    fight_final_communicate = Communicate(
        text=text,
        color=(255, 0, 0),
        font_size=42,
        coordinates=(100, 400)
    )
    render_texts([fight_final_communicate])
    time.sleep(5)


if __name__ == "__main__":
    run = True

    town_width = read_config_value("town_width")
    town_height = read_config_value("town_height")
    town = pygame.Rect(0, 0, town_width, town_height)
    town.center = (WIDTH//2, HEIGHT//2)

    player_width = read_config_value("player_width")
    player_height = read_config_value("player_height")
    player_x, player_y = generate_player_starting_point(
        area=town,
        player_width=player_width,
        player_height=player_height
    )
    p = Player(
        x=player_x,
        y=player_y,
        width=player_width,
        height=player_height,
        color=(0, 255, 255)
    )
    p2 = Player(
        x=15,
        y=15,
        width=player_width,
        height=player_height,
        color=(0, 0, 255)
    )

    score_items = generate_score_items()
    clock = pygame.time.Clock()
    score_items_thread = Thread(target=add_new_score_items, args=(score_items,), daemon=True)
    score_items_thread.start()

    while run:
        clock.tick(120)
        check_score_item_collision(score_items, p)
        if p.rect_obj.colliderect(p2.rect_obj):
            print("Collision")
            fight_screen()
            player_x, player_y = generate_player_starting_point(
                area=town,
                player_width=player_width,
                player_height=player_height
            )
            p.x = player_x
            p.y = player_y
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, p2, score_items, town)
