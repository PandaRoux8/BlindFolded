import socket

HOST = '127.0.0.1'
PORT = 37666


class Server(object):

    def __init__(self):
        self.blind = None
        self.socket = None
        self.connection = None
        self.address = None
        self.game = None

    def listen(self):
        """
        Check for move from the blind
        """
        data = self.connection.recv(256)
        if data:
            data = data.decode()
            if ';' in data:
                self.update_blind_data(data)
            elif 'map' in data:
                self.game.reload_game()

    def start_server(self):
        """
        Start the server
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(37666)
        self.connection, self.address = self.socket.accept()

    def update_blind_data(self, data):
        """
        Update the blind position
        :param data: x and y position as bytes and spearated by a ;
        """
        print("sah", self.blind, data)
        if self.blind:
            x, y = data.split(';')
            self.blind.update_position(x, y)

    @staticmethod
    def check_connection():
        """
        Check for a client connection
        :return: True if succes False otherwise
        """
        return True

    def __del__(self):
        """
        Destructor to close all connection when this object is destroyed
        :return:
        """
        self.connection.close()
        self.socket.close()
