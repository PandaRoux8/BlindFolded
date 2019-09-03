import socket

SERVER_IP = '127.0.0.1'
PORT = 37666


class Client(object):

    @staticmethod
    def connect():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, PORT))
        return sock

    @staticmethod
    def send_player_data(pos_x, pos_y):
        sock = Client.connect()
        # Need to send bytes
        data = ("%s;%s" % (pos_x, pos_y)).encode()
        sock.sendall(data)
        # TODO : optimize this ? Let it open always, probably, but when do we close it
        sock.close()


# Client.send_player_data(32, 64)
