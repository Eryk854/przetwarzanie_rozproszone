import pickle
import socket
import threading

from configuration.read_config_value import read_config_value
from fight import Fight


def handle_client(conn, fight_player_number: int, fight_id: int) -> None:
    while True:
        fight_score = int.from_bytes(conn.recv(2048), "little")
        fight = fights[fight_id]
        fight.result[fight_player_number] = fight_score
        while None in fight.result:
            pass
        fight.take_fight_result()
        player_win = fight.player_win(fight_player_number)
        text = fight.text_to_user(player_win)
        player_win = int(player_win)

        send_dict = pickle.dumps({"player_win": player_win, "user_text": text})
        conn.send(send_dict)
        break
    print("Fight thread ends")


def main_thread(conn) -> None:
    global id_count
    print("Connected to fight server")
    while True:
        data = conn.recv(2048).decode()
        if data == "fight":
            id_count += 1
            fight_player_number = 0
            fight_id = (id_count - 1) // 2

            if id_count % 2 == 1:
                fights[fight_id] = Fight()
                print("Creating a new fight ...")
            else:
                fight_player_number = 1
            thread = threading.Thread(target=handle_client, args=(conn, fight_player_number, fight_id))
            thread.start()
            thread.join()


if __name__ == "__main__":
    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = read_config_value("fight_server_port")
    ADDR = (SERVER, PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}, port: {PORT}")

    id_count = 0
    fights = {}
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=main_thread, args=(conn,))
        thread.start()
