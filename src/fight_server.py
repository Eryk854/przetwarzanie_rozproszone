import math
import pickle
import random
import socket
import threading
import time
from typing import List, Tuple

from pygame.color import Color
from pygame.rect import Rect

from fight import Fight
from player import Player
from read_config_value import read_config_value
from score_item import ScoreItem

HEADER = 64
PORT = 5052
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def handle_client(conn, p, game_id) -> None:
    send_dict = {"p": p, "fight": Fight(game_id)}
    conn.send(pickle.dumps(send_dict))
    while True:
        recv_dict = pickle.loads(conn.recv(2048))
        result = recv_dict["fight"]
        player = recv_dict["p"]
        fight = fights[game_id]
        fight.result[player] = result
        print(fight.result)
        while None in fight.result:
            pass
        fight.take_winner()

        if (p == 0 and fight.winner == 0) or (p == 1 and fight.winner == 1):
            result = 1
        else:
            result = 0

        send_dict = pickle.dumps({"result": result})
        conn.send(send_dict)
        conn.close()
        break


if __name__ == "__main__":
    server.listen()
    id_count = 0
    fights = {}
    while True:
        conn, addr = server.accept()
        current_connection = threading.activeCount() - 1

        id_count += 1
        p = 0
        game_id = (id_count - 1) // 2

        if id_count % 2 == 1:
            fights[game_id] = Fight(game_id)
            print("Creating a new game ...")
        else:
            fights[game_id].ready = True
            p = 1
        print(id_count)
        print(p)
        thread = threading.Thread(target=handle_client, args=(conn, p, game_id))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {current_connection}")