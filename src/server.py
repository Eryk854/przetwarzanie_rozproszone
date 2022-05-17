import math
import pickle
import random
import socket
import threading
import time
from typing import List, Tuple

from pygame.color import Color
from pygame.rect import Rect

from enums.color_values import ColorValue
from configuration.read_config_value import read_config_value
from helper import get_town
from player import Player

from score_item import ScoreItem


def generate_score_item() -> ScoreItem:
    radius = random.randrange(5, 20, 5)
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    while (x + radius >= WIDTH) or (x - radius <= 0):
        x = random.randint(0, WIDTH)
    while (y + radius >= HEIGHT) or (y - radius <= 0):
        y = random.randint(0, HEIGHT)

    score_value = 25 - radius
    color = Color(150, 105, 150)
    return ScoreItem(x, y, radius, color, score_value)


def generate_score_items(elements: int = 10) -> List[ScoreItem]:
    score_items = []
    for _ in range(elements):
        score_item = generate_score_item()
        score_items.append(score_item)
    return score_items


def add_new_score_items(score_items: List[ScoreItem]) -> None:
    sleep_time = read_config_value("score_item_time")
    while True:
        if len(score_items) < 50:
            score_item = generate_score_item()
            score_items.append(score_item)
        time.sleep(sleep_time)

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
            print(player.points)


def generate_player_starting_point(
        area: Rect, player_width: int, player_height: int
) -> Tuple[int, int]:
    x = random.randint(area.left, area.right - player_width)
    y = random.randint(area.top, area.bottom - player_height)
    return x, y


def handle_client(conn, addr, player_id: int, score_items: List[ScoreItem]) -> None:
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send(pickle.dumps(players[player_id]))
    connected = True
    while connected:
        try:
            data = pickle.loads(conn.recv(2048 * 2))
            players[player_id] = data
            check_score_item_collision(score_items, players[player_id])

            players_copy = players.copy()
            del players_copy[player_id]
            players_copy = list(players_copy.values())
            send_dict = {"players": players_copy, "score_items": score_items, "player": players[player_id]}
            conn.send(pickle.dumps(send_dict))
        except Exception as e:
            print(e)
            break
    del players[player_id]
    print("Active players: ", len(players))
    print("Lost connection")
    conn.close()


if __name__ == "__main__":
    PORT = read_config_value("server_port")
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}, port: {PORT}")

    WIDTH = read_config_value("screen_width")
    HEIGHT = read_config_value("screen_height")
    town = get_town()
    player_width = read_config_value("player_width")
    player_height = read_config_value("player_height")

    score_items = generate_score_items()
    score_items_thread = threading.Thread(target=add_new_score_items, args=(score_items,), daemon=True)
    score_items_thread.start()

    players = {}
    player_id = 0
    while True:
        conn, addr = server.accept()
        player_x, player_y = generate_player_starting_point(
            area=town,
            player_width=player_width,
            player_height=player_height
        )
        player = Player(
            x=player_x,
            y=player_y,
            width=player_width,
            height=player_height,
            color=ColorValue.BLUE.value
        )
        players[player_id] = player
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_id, score_items))
        thread.start()
        player_id += 1
