import pickle
import random
import socket
import time
from threading import Thread
from typing import List, Tuple

import pygame
from pygame import font, display, draw
from pygame.color import Color
from pygame.rect import Rect

from color_values import ColorValue
from communicate import Communicate
from read_config_value import read_config_value
from src.player import Player
from src.score_item import ScoreItem

font.init()

HEADER = 64
PORT = 5051
PORT1 = 5052
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.17.240.1"
ADDR = (SERVER, PORT)
ADDR2 = (SERVER, PORT1)

WIDTH = read_config_value("screen_width")
HEIGHT = read_config_value("screen_height")
win = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Client")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
fight_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def redraw_window(
    win, player: Player, players: List[Player], score_items: List[ScoreItem], town: Rect
) -> None:
    win.fill((255, 255, 255))
    draw.rect(win, (200, 200, 200), town)
    player.draw(win)
    for p in players:
        p.color = ColorValue.RED.value
        p.draw(win)

    for score_item in score_items:
        draw.circle(
            surface=win,
            color=score_item.color,
            center=score_item.coordinates,
            radius=score_item.radius
        )

    font = pygame.font.SysFont(name="comicsans", size=24)
    img = font.render(f"Your result: {player.points}", True, (255, 255, 0), None)
    win.blit(img, (0, WIDTH-50))

    display.update()


def generate_player_starting_point(
        area: Rect, player_width: int, player_height: int
) -> Tuple[int, int]:
    x = random.randint(area.left, area.right - player_width)
    y = random.randint(area.top, area.bottom - player_height)
    return x, y


def render_texts(communicates: List[Communicate]) -> None:
    win.fill(Color(255, 255, 255))
    for communicate in communicates:
        font = pygame.font.SysFont(communicate.font_name, communicate.font_size)
        text = font.render(communicate.text, communicate.antialias, communicate.color)
        win.blit(text, communicate.coordinates)
    display.update()


def fight_wait_screen():
    fight_time_wait = read_config_value("fight_time_wait")
    fight_init_communicate = Communicate(
        text="Fight screen! Press Enter button to win",
        color=Color(255, 0, 0),
        font_size=42,
        coordinates=(100, 200)
    )
    render_texts([fight_init_communicate])
    start_ticks = pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        fight_count_communicate = Communicate(
            text=f"Fight starts in {round(fight_time_wait - seconds, 2)}",
            color=Color(255, 0, 0),
            font_size=42,
            coordinates=(100, 400)
        )
        render_texts([fight_init_communicate, fight_count_communicate])
        if seconds > fight_time_wait:
            break


def fight_screen(player: Player):
    fight_init_communicate = Communicate(
        text="Fight screen! Press Enter button to win",
        color=Color(255, 0, 0),
        font_size=42,
        coordinates=(100, 200)
    )

    render_texts([fight_init_communicate])
    start_ticks = pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        fight_count_communicate = Communicate(
            text=f"Fight starts in {round(5 - seconds, 2)}",
            color=Color(255, 0, 0),
            font_size=42,
            coordinates=(100, 400)
        )
        render_texts([fight_init_communicate, fight_count_communicate])
        if seconds > 5:
            break
    start_fight_communicate = Communicate(
        text=f"Start fight! Press Enter button to win",
        color=Color(255, 0, 0),
        font_size=42,
        coordinates=(100, 400)
    )
    render_texts([start_fight_communicate])

    fight_time = read_config_value("fight_time")
    timeout = time.time() + fight_time
    count = 0

    pygame.event.clear()
    while time.time() < timeout:
        fight_count_communicate = Communicate(
            text=f"You press Enter: {count} times",
            color=Color(255, 0, 0),
            font_size=42,
            coordinates=(100, 400)
        )
        render_texts([fight_init_communicate, fight_count_communicate])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                count += 1

    send_fight(count)
    recv_dict = pickle.loads(fight_client.recv(2048))
    result = recv_dict["result"]

    if result:
        text = "You won!!"
        player.fight_result_points(True)
    else:
        text = "You lose :("
        player.fight_result_points(False)
    fight_final_communicate = Communicate(
        text=text,
        color=Color(255, 0, 0),
        font_size=42,
        coordinates=(100, 400)
    )
    render_texts([fight_final_communicate])
    time.sleep(5)


def send(player: Player):
    client.send(pickle.dumps(player))


def send_fight(fight_score: int):
    fight_score = fight_score.to_bytes(32, "little")
    fight_client.send(fight_score)


if __name__ == "__main__":
    run = True

    client.connect(ADDR)
    fight_client.connect(ADDR2)

    player = pickle.loads(client.recv(2048 * 2))
    clock = pygame.time.Clock()

    town_width = read_config_value("town_width")
    town_height = read_config_value("town_height")
    town = Rect(0, 0, town_width, town_height)
    town.center = (WIDTH // 2, HEIGHT // 2)

    player_width = read_config_value("player_width")
    player_height = read_config_value("player_height")

    while run:
        clock.tick(120)
        send(player)
        received_dict = pickle.loads(client.recv(2048 * 2))
        player = received_dict["player"]
        players = received_dict["players"]
        score_items = received_dict["score_items"]

        for p in players:
            if (not town.collidepoint(player.rect_obj.center)) and (not town.collidepoint(p.rect_obj.center)):
                if player.rect_obj.colliderect(p.rect_obj) and not p.fight:
                    pygame.time.delay(100)
                    player.fight = True
                    send(player)
                    received_dict = pickle.loads(client.recv(2048 * 2))
                    player = received_dict["player"]
                    players = received_dict["players"]
                    score_items = received_dict["score_items"]

                    fight_client.send(b"fight")
                    fight_screen(player)
                    player_x, player_y = generate_player_starting_point(
                        area=town,
                        player_width=player_width,
                        player_height=player_height
                    )
                    player.x = player_x
                    player.y = player_y
                    player.fight = False
                    pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player.move()
        redraw_window(win, player, players, score_items, town)
