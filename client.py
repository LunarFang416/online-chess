import socket 
import pickle
import time

HEADER = 4096
PORT = 5050
FORMAT = 'utf-8'
SERVER = "localhost"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect()


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.board = self.connect()
        self.board = pickle.loads(self.board)

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(HEADER*8)

    def disconnect(self, data):
        self.client.close()
        try:
            self.client.send(pickle.dumps(data))
            reply = self.client.recv(HEADER*8)
        except Exception as e:
            print(e)

        return reply
    
    # maybe we can also use this function as well (we can put the last part of the disconnect function here)?
    def send(self,info,pick=False):
        if pick:
            try:
                self.client.send(pickle.dumps(data))
                reply=self.client.recv(HEADER*8)
            except Exception as e:
                print(e)
        return reply 
            
            
        
