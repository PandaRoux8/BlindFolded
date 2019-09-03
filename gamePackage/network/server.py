import socket

HOST = '127.0.0.1'
PORT = 37666


class Server(object):

    def __init__(self):
        self.player = None

    @staticmethod
    def start_server():
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
                    Server.update_player_data(data)

    @staticmethod
    def update_player_data(data):
        x, y = data.decode().split(';')
        # TODO : Update the player object with these data

    @staticmethod
    def check_connection():
        pass


# # TODO : remove this and start it when you get in the lobby
# Server().start_server()
