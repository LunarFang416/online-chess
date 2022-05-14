import socket
import threading
import pickle

HEADER = 4096
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
WHITE, BLACK = 1, 0
CURRENT_GAMES = [[]]
CONNECTION_ADDED = "!CONNECTION_ADDED"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def all_games_full(current_games):
    for game in current_games:
        if len(game) != 2: return False
    return True

def is_in_game(addr):
    for game in CURRENT_GAMES:
        for i in game:
            if i[0] == addr: return game
    
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

def broadcast(game, addr):
    if len(game) == 2:
        if game[0][0] == addr: 
            return game[1][0]
        else:
            return game[0][0]
    
    return False

def new_game(conn, addr, game):
    if broadcast(game, addr):
        msg = conn.recv(HEADER*8)
        if msg:
            if pickle.loads(msg)["data"] == DISCONNECT_MESSAGE: 
                if is_in_game(addr):
                    remove_from_game(addr)
                    print(f"[{addr[1]} REMOVED] {addr} removed")
                    conn.close()
                else: 
                    print(f"[{addr[1]} ERROR] while removing {addr}")
            else: 
                print(f"{addr[1]} herrrrrrr")
                for clients in game:
                    clients[1].sendall(msg)

            # print(f"[{addr[1]}] {pickle.loads(msg)}")

    

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        if not is_in_game(addr):
            print(f"[{addr[1]} ADDING] {addr} to a game")
            if all_games_full(CURRENT_GAMES): CURRENT_GAMES.append([])
            for game in CURRENT_GAMES:
                if len(game) == 0:
                    game.append((addr, conn, WHITE))
                    conn.send(pickle.dumps({"type": CONNECTION_ADDED, "color": WHITE, "game": len(game)}))
                elif len(game) == 1:
                    game.append((addr, conn, BLACK))
                    conn.send(pickle.dumps({"type": CONNECTION_ADDED, "color":BLACK, "game": len(game)}))
            print(f"[{addr[1]} TOTAL ACTIVE GAMES] {len(CURRENT_GAMES)}")
        
        new_game(conn, addr, is_in_game(addr))

def start():
    global CONNECTIONS
    CONNECTIONS = 0
    print(CURRENT_GAMES)
    print(f"[STARTING] server is starting on port {PORT}")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[{addr[1]} ACTIVE CONNECTIONS] {threading.active_count() - 1}")

start()
