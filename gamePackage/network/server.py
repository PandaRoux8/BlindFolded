import socket

HOST = '127.0.0.1'
PORT = 37666


class Server(object):

    def __init__(self):
        self.player = None

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(37666)
            conn, addr = s.accept()
            with conn:
                print("Connected by " + str(addr))
                while True:
                    data = conn.recv(256)
                    if not data:
                        break
                    else:
                        self.update_player_data(data)

    def update_player_data(self, data):
        print("sah", self.player, data)
        if self.player:
            x, y = data.decode().split(';')
            self.player.update_position(x, y)
        # TODO : Update the player object with these data

    @staticmethod
    def check_connection():
        pass


# # TODO : remove this and start it when you get in the lobby
# Server().start_server()
