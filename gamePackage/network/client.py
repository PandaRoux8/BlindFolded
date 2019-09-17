import socket

SERVER_IP = '127.0.0.1'
PORT = 37666


class Client(object):

    def __init__(self):
        self.socket = self.connect()

    @staticmethod
    def connect():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))
        return sock

    def send_new_map(self, map):
        map = "load_map:%s" % map
        data = map.encode()
        self.socket.sendall(data)

    def send_reload_game(self):
        data = "game_reload:".encode()
        self.socket.sendall(data)

    def send_blind_data(self, pos_x, pos_y):
        # Need to send bytes
        data = ("%s;%s" % (pos_x, pos_y)).encode()
        self.socket.sendall(data)

    def __del__(self):
        self.socket.close()

# Client.send_player_data(32, 64)
