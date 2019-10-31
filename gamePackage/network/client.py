# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

import socket
from time import sleep
import constants


class Client(object):

    def __init__(self, server_ip):
        """
        :param server_ip: string representing server IP
        """
        self._server_ip = server_ip
        self._socket = self.connect(server_ip)
        self.game = None

    @staticmethod
    def connect(server_ip):
        """
        Create a socket and connect to the server
        :param server_ip: string representing server IP
        :return: .Socket object
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, constants.PORT))
        sock.settimeout(0.01)
        return sock

    def send_new_map(self, map, map_timer):
        """
        Send the name of the loaded map to the server and the timer for the map
        :param map: string of the map's name
        :param map_timer: int timer of the map
        """
        map = "load_map:%s$map_timer:%s$" % (map, map_timer)
        data = map.encode()
        self._socket.sendall(data)

    def send_reload_game(self):
        """
        Send data to the server to reload the game
        """
        data = "game_reload:$".encode()
        self._socket.sendall(data)

    def send_blind_data(self, pos_x, pos_y):
        """
        Send data to the server to update the blind position
        :param pos_x: int of x axis position
        :param pos_y: int of y axis position
        """
        data = ("%s;%s$" % (pos_x, pos_y)).encode()
        self._socket.sendall(data)

    def send_display_game_over(self):
        """
        Send data to the server to display the game_over message
        """
        data = "game_over:$".encode()
        self._socket.sendall(data)

    def send_display_next_level(self):
        """
        Send data to the server to display the next_level message
        """
        data = "next_level:$".encode()
        self._socket.sendall(data)

    def send_pause_game(self):
        data = "pause_game$".encode()
        self._socket.sendall(data)

    def get_pause_game(self):
        try:
            data = self._socket.recv(256)
        except socket.timeout as e:
            data = None

        if data:
            data_wo_trail = data.decode().split('$')
            # Remove last index as split() leaves an empty char at the end
            del data_wo_trail[-1]
            for data in data_wo_trail:
                if data == 'pause_game':
                    self.game.pause_game()

    def check_server_ready(self):
        """
        Check if the Guide is ready when we ask him to press space to get to the next level or retry the level
        """
        while True:
            # Send the message until the server gives an answer
            data = "client_ready$".encode()
            self._socket.sendall(data)
            try:
                data = self._socket.recv(256)
            except socket.timeout as e:
                data = None

            # print(data)
            if data:
                data = data.decode()
                if data.count('$') == 1:
                    data = data[:-1]
                    if 'server_ready' in data:
                        break
            # Sleep so we don't flood the server
            sleep(0.5)

    def release(self):
        """
        Close the connection for the client
        """
        self._socket.close()
