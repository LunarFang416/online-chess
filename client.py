import socket 
import pickle
from board import Board
import json

HEADER = 4096
PORT = 5050
FORMAT = 'utf-8'
SERVER = "localhost"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client.connect()

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.board = self.connect()
        self.board = Board(self.board)
        self.color = None

    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.send("Pinging to server"))

    def disconnect(self):
        self.client.close()

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            reply = self.client.recv(HEADER*8)
            print(pickle.loads(reply))
        except Exception as e:
            print(e)

        return reply

c = Client()
print(c.board)
input()
c.send({"data": c.board.board})
# c.send(DISCONNECT_MESSAGE)
