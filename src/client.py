import pickle
import random
import socket
import time
from typing import List, Tuple

import pygame
from pygame import font, display, draw
from pygame.color import Color
from pygame.rect import Rect
from pygame.surface import Surface

from configuration.read_config_value import read_config_value
from enums.color_values import ColorValue
from communicate import Communicate
from helper import get_town
from src.player import Player
from src.score_item import ScoreItem

font.init()


def redraw_window(
    win: Surface, player: Player, players: List[Player], score_items: List[ScoreItem], town: Rect
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
    player_result_communicate = Communicate(
        text=f"Your result: {player.points}",
        color=ColorValue.YELLOW.value,
        font_size=36,
        coordinates=(0, WIDTH-50)
    )
    player_result_communicate.render_communicate(win, False)


def generate_player_starting_point(
        area: Rect, player_width: int, player_height: int
) -> Tuple[int, int]:
    x = random.randint(area.left, area.right - player_width)
    y = random.randint(area.top, area.bottom - player_height)
    return x, y


def fight_wait_screen():
    fight_time_wait = read_config_value("fight_time_wait")
    fight_init_communicate = Communicate(
        text="Fight screen! Press Enter button to win",
        color=ColorValue.RED.value,
        font_size=42,
        coordinates=(100, 200)
    )
    fight_init_communicate.render_communicate(win, True)
    start_ticks = pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        fight_count_communicate = Communicate(
            text=f"Fight starts in {round(fight_time_wait - seconds, 2)}",
            color=ColorValue.RED.value,
            font_size=42,
            coordinates=(100, 400)
        )
        Communicate.render_multiple_communicates([fight_init_communicate, fight_count_communicate], win)
        if seconds > fight_time_wait:
            break


def fight_screen(player: Player):
    fight_init_communicate = Communicate(
        text="Fight screen! Press Enter button to win",
        color=Color(255, 0, 0),
        font_size=36,
        coordinates=(100, 200)
    )
    fight_init_communicate.render_communicate(win, True)
    start_ticks = pygame.time.get_ticks()
    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        fight_count_communicate = Communicate(
            text=f"Fight starts in {round(5 - seconds, 2)}",
            color=Color(255, 0, 0),
            font_size=42,
            coordinates=(100, 400)
        )
        Communicate.render_multiple_communicates([fight_init_communicate, fight_count_communicate], win)
        if seconds > 5:
            break
    fight_time = read_config_value("fight_time")
    timeout = time.time() + fight_time
    count = 0

    pygame.event.clear()
    pygame.event.get()
    while time.time() < timeout:

        fight_count_communicate = Communicate(
            text=f"You press Enter: {count} times",
            color=Color(255, 0, 0),
            font_size=42,
            coordinates=(100, 400)
        )
        Communicate.render_multiple_communicates([fight_init_communicate, fight_count_communicate], win)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                count += 1

    send_fight_score(count)
    recv_dict = pickle.loads(fight_client.recv(2048))
    player_win = recv_dict["player_win"]
    user_text = recv_dict["user_text"]
    player.fight_result_points(player_win)

    fight_final_communicate = Communicate(
        text=user_text,
        color=ColorValue.RED.value,
        font_size=42,
        coordinates=(100, 400)
    )
    fight_final_communicate.render_communicate(win, True)
    time.sleep(5)


def chceck_if_players_fight() -> bool:
    for p in players:
        if (not town.collidepoint(player.rect_obj.center)) and (not town.collidepoint(p.rect_obj.center)):
            if player.rect_obj.colliderect(p.rect_obj) and not p.fight:
                return True
    return False


def send_to_server(player: Player) -> None:
    client.send(pickle.dumps(player))


def send_fight_score(fight_score: int) -> None:
    fight_score = fight_score.to_bytes(32, "little")
    fight_client.send(fight_score)


def send_fight() -> None:
    fight_client.send(b"fight")


if __name__ == "__main__":
    SERVER_PORT = read_config_value("server_port")
    FIGHT_SERVER_PORT = read_config_value("fight_server_port")
    SERVER = read_config_value("server_ip")
    FIGHT_SERVER = read_config_value("fight_server_ip")
    SERVER_ADDR = (SERVER, SERVER_PORT)
    FIGHT_SERVER_ADDR = (SERVER, FIGHT_SERVER_PORT)

    WIDTH = read_config_value("screen_width")
    HEIGHT = read_config_value("screen_height")
    window_caption = read_config_value("window_caption")
    win = display.set_mode((WIDTH, HEIGHT))
    display.set_caption(window_caption)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fight_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(SERVER_ADDR)
    fight_client.connect(FIGHT_SERVER_ADDR)

    town = get_town()
    player_width = read_config_value("player_width")
    player_height = read_config_value("player_height")

    player = pickle.loads(client.recv(2048 * 2))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(120)
        send_to_server(player)
        received_dict = pickle.loads(client.recv(2048 * 2))
        player = received_dict["player"]
        players = received_dict["players"]
        score_items = received_dict["score_items"]
        fight_flag = chceck_if_players_fight()

        if fight_flag:
            pygame.time.delay(100)
            player.fight = True
            send_to_server(player)
            received_dict = pickle.loads(client.recv(2048 * 4))
            player = received_dict["player"]
            players = received_dict["players"]
            score_items = received_dict["score_items"]

            send_fight()
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
