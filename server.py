import socket
import threading
import pickle
import json
import selectors


HEADER = 4096
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
WHITE, BLACK = 1, 0
CURRENT_GAMES = [[]]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def all_games_full(current_games):
    for game in current_games:
        if len(game) != 2: return False
    return True

def is_in_game(addr):
    for game in CURRENT_GAMES:
        for i in game:
            for key in i.keys():
                if key == addr: 
                    return True
    
    return False

def remove_from_game(addr):
    for game in CURRENT_GAMES:
        for i in game:
            for key in i.keys():
                if key == addr: 
                    del game[game.index(i)]
                    temp = game
                    CURRENT_GAMES.remove(game)
                    CURRENT_GAMES.append(temp)
                    return False


def handle_client(conn, addr, CONNECTIONS):
    CONNECTIONS += 1
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg = conn.recv(HEADER*8)
        if not is_in_game(addr):
            print(f"[ADDING] {addr} to a game")
            if all_games_full(CURRENT_GAMES): CURRENT_GAMES.append([])
            for game in CURRENT_GAMES:
                if len(game) == 0:
                    game.append({addr: WHITE})
                    conn.send(pickle.dumps(WHITE))
                elif len(game) == 1:
                    game.append({addr: BLACK})
                    conn.send(pickle.dumps(BLACK))
            print(f"[TOTAL ACTIVE GAMES] {len(CURRENT_GAMES)}")
        if msg:
            if pickle.loads(msg) == DISCONNECT_MESSAGE: 
                if is_in_game(addr):
                    remove_from_game(addr)
                    print(f"[REMOVED] {addr} removed")
                else: 
                    print(f"[ERROR] while removing {addr}")
                connected = False
                break
            print(f"[{addr}] {pickle.loads(msg)}")

    conn.close()

def start():
    global CONNECTIONS
    CONNECTIONS = 0
    print(f"[STARTING] server is starting on port {PORT}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, CONNECTIONS))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {CONNECTIONS + 1}")


#  def client_threading(conn):

#         global playerID, connections
#         if(connections%2):
#             playerID="white"
#         else:
#             playerID="Black"
            
        
#         data_string=pickle.dumps(playerID)
#         while(true):
            
            
# start()
