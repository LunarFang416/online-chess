import socket 
import pickle
from board import Board
import threading

HEADER = 4096
PORT = 5050
FORMAT = 'utf-8'
SERVER = "localhost"
DISCONNECT_MESSAGE = "!DISCONNECT"
CONNECTION_ADDED = "!CONNECTION_ADDED"
BOARD_UPDATE = "!BOARD_UPDATE"
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
        self.color = None
        self.in_game = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()


    def connect(self):
        self.client.connect(self.addr)
        return self.send({"type":CONNECTION_ADDED, "data": CONNECTION_ADDED})

    def disconnect(self):
        self.client.close()
        self.in_game = False
        self.send({"type":"msg", "data": DISCONNECT_MESSAGE})

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = pickle.loads(self.client.recv(HEADER*8))
            print(reply)
            return reply
        except Exception as e:
            print(e)


    def listen(self):
        while True and self.in_game:
            data = pickle.loads(self.client.recv(HEADER*8))
            print(data)
            if data["type"] == CONNECTION_ADDED: 
                self.game += 1
            
            if data["type"] == BOARD_UPDATE:
                self.board.board = data["data"]