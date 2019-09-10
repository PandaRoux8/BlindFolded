import socket

HOST = '127.0.0.1'
PORT = 37666


class Server(object):

    def __init__(self):
        self.player = None
        self.socket = None
        self.connection = None
        self.address = None
        self.game = None

    def listen(self):
        """
        Check for move from the player
        """
        data = self.connection.recv(256)
        if data:
            data = data.decode()
            if ';' in data:
                self.update_player_data(data)
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

    def update_player_data(self, data):
        """
        Update the player position
        :param data: x and y position as bytes and spearated by a ;
        """
        print("sah", self.player, data)
        if self.player:
            x, y = data.split(';')
            self.player.update_position(x, y)

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
