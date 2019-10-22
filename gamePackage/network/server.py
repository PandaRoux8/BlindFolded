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
        self.map = None

    def listen(self):
        """
        Check for move from the blind
        """
        data = self.connection.recv(256)
        if data:
            print(data)
            data = data.decode()
            if data.count('$') == 1:
                # Remove trailing char $
                data = data[:-1]
                self.read_data(data)
            else:
                datas = data.split('$')
                print("Datas", datas)
                # Remove last index as split() leaves an empty char at the end
                del datas[-1]
                for data in datas:
                    # Remove trailing char $
                    self.read_data(data)

    def read_data(self, data):
        if ';' in data:
            self.update_blind_data(data)
        elif 'load_map:' in data:
            print("MAP", data)
            self.map = data.split('load_map:')[1]
        elif 'game_reload:' in data:
            self.map = None
            self.game.reload_game()
        elif 'game_over:' in data:
            self.game.game_over()
        elif 'next_level:' in data:
            self.game.next_level()
        elif 'client_ready' in data:
            pass

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
        if self.blind:
            x, y = data.split(';')
            self.blind.update_position(x, y)

    def check_client_ready(self):
        while True:
            data = self.connection.recv(256)
            print(data)
            if data:
                data = data.decode()
                if data.count('$') == 1:
                    data = data[:-1]
                    if data == 'client_ready':
                        server_data = 'server_ready$'.encode()
                        self.connection.sendall(server_data)
                        break

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

    def release(self):
        self.connection.close()
        self.socket.close()
