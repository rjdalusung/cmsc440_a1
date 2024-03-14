#ChatClient.py

from socket import *
import sys


args = sys.argv
if len(args) != 5:
    print("Usage: python ChatClient.py HOSTNAME PORT NICKNAME CLIENT_ID")
    exit()

HOST = args[1]
PORT = int(args[2])
NICKNAME = args[3]
CLIENT_ID = int(args[4])

#Create the socket and connect
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((HOST,PORT))

#Client input
clientString = input("Enter Message:\n")

#Send the client input to server
clientSocket.send(clientString.encode())

#Read line from Server
serverString = clientSocket.recv(1024)
serverString = serverString.decode()
print("Server:", serverString)

clientSocket.close()