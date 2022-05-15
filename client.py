import socket, pickle, threading
from board import Board

HEADER = 4096
PORT = 5050
SERVER = "localhost"
DISCONNECT_MESSAGE = "!DISCONNECT"
CONNECTION_ADDED = "!CONNECTION_ADDED"
CONNECTION_REMOVED = "!CONNECTION_REMOVED"
BOARD_UPDATE = "!BOARD_UPDATE"
COLOR_CHANGE = "!COLOR_CHANGE"
GAME_OVER = "!GAME_OVER"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.data = self.connect()
        self.board = Board(self.data["color"])
        self.game = self.data["game"]
        self.color = self.data["color"]
        self.game_over = False
        self.win = False
        self.in_game = True
        self.your_move = self.data["color"]
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def connect(self):
        self.client.connect(self.addr)
        return self.send({"type":CONNECTION_ADDED, "data": CONNECTION_ADDED})

    def disconnect(self):
        self.send({"type": DISCONNECT_MESSAGE})
        self.client.close()

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(HEADER*8))
            return reply
        except Exception as e:
            print(e)

    def listen(self):
        while self.in_game:
            data = pickle.loads(self.client.recv(HEADER*8))
            if data["type"] == CONNECTION_ADDED: 
                self.game += 1
            
            if data["type"] == GAME_OVER:
                self.board.board = data["data"]
                self.game_over = True
                self.win = data["win"]
            
            if data["type"] == BOARD_UPDATE:
                self.board.board = data["data"]
                self.your_move = data["move"]
            
            if data["type"] == DISCONNECT_MESSAGE:
                self.in_game = False
                break
            
            if data["type"] == CONNECTION_REMOVED:
                self.game = data["data"]
                self.color = data["data"]
                self.your_move = data["data"]
                self.win = False
                self.game_over = False