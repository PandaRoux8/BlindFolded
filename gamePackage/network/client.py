import socket
from time import sleep

# SERVER_IP = '127.0.0.1'
PORT = 37666


class Client(object):

    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.socket = self.connect(server_ip)

    @staticmethod
    def connect(server_ip):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, PORT))
        return sock

    def send_new_map(self, map, map_timer):
        map = "load_map:%s$map_timer:%s$" % (map, map_timer)
        data = map.encode()
        self.socket.sendall(data)

    def send_reload_game(self):
        data = "game_reload:$".encode()
        self.socket.sendall(data)

    def send_blind_data(self, pos_x, pos_y):
        # Need to send bytes
        data = ("%s;%s$" % (pos_x, pos_y)).encode()
        self.socket.sendall(data)

    def send_display_game_over(self):
        data = "game_over:$".encode()
        self.socket.sendall(data)
        # Wait for guide

    def send_display_next_level(self):
        data = "next_level:$".encode()
        self.socket.sendall(data)

    def check_server_ready(self):
        while True:
            data = "client_ready$".encode()
            self.socket.sendall(data)
            data = self.socket.recv(256)
            print(data)
            if data:
                data = data.decode()
                if data.count('$') == 1:
                    data = data[:-1]
                    if 'server_ready' in data:
                        break
            # Sleep so we don't flood the server
            sleep(0.5)

    def __del__(self):
        self.socket.close()

    def release(self):
        self.socket.close()
