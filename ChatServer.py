#ChatServer.py

from socket import *
import sys

if len(args) != 2:
    print("Usage: python ChatServer.py port")
    exit()

port = int(args[1])

welcomeSocket = socket(AF_INET, SOCK_STREAM)
welcomeSocket.bind(('', port))
welcomeSocket.listen(1)

while 1:

    connectionSocket, addr = welcomeSocket.accept()
    print("Client Connected\n")

    clientString = connectionSocket.recv(1024)
    clientString = clientString.decode()
    print("Client:",clientString)

    serverString = "Received \"" + clientString + "\"\n"


    connectionSocket.send(serverString.encode())

    connectionSocket.close()