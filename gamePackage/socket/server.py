# coding: utf-8
import socket

HOST = ''
PORT = 37666


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(37666)
    conn, addr = s.accept()
    with conn:
        print("Connected by " + str(addr))
        while True:
            data = conn.recv(102)
            if not data:
                break
            print(data)
            conn.sendall(data)
