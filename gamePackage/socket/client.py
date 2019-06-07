# coding: utf-8
import socket

SERVER_IP = '192.168.1.134'
PORT = 37666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, PORT))
    s.sendall('Hello my g')
    data = s.recv(1024)

print("Received", repr(data))
