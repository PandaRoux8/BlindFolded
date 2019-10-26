import socket
from gamePackage import constants


class Server(object):

    def __init__(self, client_ip):
        self._client_ip = client_ip
        self.blind = None
        self._socket = None
        self._connection = None
        self._address = None
        self.game = None
        self.map = None
        self.map_timer = None

    def __del__(self):
        """
        Destructor to close all connection when this object is destroyed
        """
        self._connection.close()
        self._socket.close()

    def start_server(self):
        """
        Start the server
        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._client_ip, constants.PORT))
        self._socket.listen(constants.PORT)
        self._connection, self._address = self._socket.accept()
        # Set a timeout on the connection otherwise the system will be stuck on recv() until it receive some data
        self._connection.settimeout(constants.SOCKET_TIMEOUT)

    def listen(self):
        """
        Listen for the data sent by the client
        """
        try:
            # If we don't receive any data during the timeout an exception is raised, we just need to wait until we have
            # a data, and not being stuck on receive
            data = self._connection.recv(256)
        except socket.timeout:
            data = None
        if data:
            # print(data)
            data = data.decode()
            if data.count('$') == 1:
                # Remove trailing char $
                data = data[:-1]
                self._read_data(data)
            else:
                datas = data.split('$')
                print(datas)
                # Remove last index as split() leaves an empty char at the end
                del datas[-1]
                for data in datas:
                    # Remove trailing char $
                    self._read_data(data)

    def _read_data(self, data):
        """
        Read the data sent by the client
        :param data: string of data sent by the client
        """
        if ';' in data:
            self._update_blind_position(data)
        elif 'load_map:' in data:
            self.map = data.split('load_map:')[1]
        elif 'map_timer:' in data:
            self.map_timer = data.split('map_timer:')[1]
        elif 'game_reload:' in data:
            self.map = None
            self.game.reload_game()
        elif 'game_over:' in data:
            self.game.game_over()
        elif 'next_level:' in data:
            self.game.next_level()

    def _update_blind_position(self, data):
        """
        Update the blind position
        :param data: x and y position as string and separated by a ;
        """
        print("Yo", data)
        if self.blind:
            x, y = data.split(';')
            print(self.blind)
            self.blind.update_position(x, y)

    def check_client_ready(self):
        while True:
            data = self._connection.recv(256)
            # print(data)
            if data:
                data = data.decode()
                if data.count('$') == 1:
                    data = data[:-1]
                    if data == 'client_ready':
                        server_data = 'server_ready$'.encode()
                        self._connection.sendall(server_data)
                        break

    @staticmethod
    def check_connection():
        """
        Check for a client connection
        :return: True if succes False otherwise
        """
        # TODO : implement this
        return True

    def release(self):
        self._connection.close()
        self._socket.close()
