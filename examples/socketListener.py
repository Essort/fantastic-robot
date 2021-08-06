
from time import sleep
import socket
import sys

HOST, PORT = "localhost", 18636
data = ''

socketClient = socket

def buffered_readLine(socket):
    line = ""
    while True:
        part = socket.recv(1)
        if part != "\n":
            line+=part
        elif part == "\n":
            break
    return line

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    while True:
        data = sock.recv(1024)
        if data:
            print("Received: {}".format(data))
        else:
            break
