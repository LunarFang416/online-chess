import socket, threading, pickle

HEADER = 4096
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
WHITE, BLACK = 1, 0
CURRENT_GAMES = [[]]
CONNECTION_ADDED = "!CONNECTION_ADDED"
CONNECTION_REMOVED = "!CONNECTION_REMOVED"
COLOR_CHANGE = "!COLOR_CHANGE"
GAME_OVER = "!GAME_OVER"

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
            if i[0] == addr: 
                del game[game.index(i)]
                if len(game) == 0:
                    del CURRENT_GAMES[CURRENT_GAMES.index(game)]
                else:
                    temp = game
                    CURRENT_GAMES.remove(game)
                    CURRENT_GAMES.append(temp)
                    return False

def new_game(conn, addr, game):
    msg = conn.recv(HEADER*8)
    print(pickle.loads(msg))
    if msg:
        if pickle.loads(msg)["type"] == DISCONNECT_MESSAGE: 
            if is_in_game(addr):
                print(f"[{addr[1]} REMOVED] {addr} removed")
                print(game)
                if game:
                    for clients in game:
                        clients[1].sendall(pickle.dumps({"type": CONNECTION_REMOVED, "data": len(game) - 1}))
                remove_from_game(addr)
                return False
            else: 
                print(f"[{addr[1]} ERROR] while removing {addr}")
        elif pickle.loads(msg)["type"] == GAME_OVER:
            print(f"[{addr[1]} GAMEOVER]")
            for clients in game:
                if clients[0] != addr:
                    clients[1].sendall(msg)
        else: 
            for clients in game:
                if clients[0] != addr:
                    clients[1].sendall(msg)
    return True

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
        
        connected = new_game(conn, addr, is_in_game(addr))
    print(f"[DISCONNECTED] {addr[1]} has disconnected")
    conn.close()

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