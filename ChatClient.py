#ChatClient.py

from socket import *
import string
import sys

def signal_handler(sig, frame):
    c.close()
    sys.exit(0)
args = sys.argv
if len(args) != 5:
    print("Usage: python ChatClient.py HOSTNAME PORT NICKNAME CLIENT_ID")
    exit()
HOST = args[1]
PORT = int(args[2])
NICKNAME = args[3]
CLIENT_ID = int(args[4])
#Create the socket and connect
c = socket(AF_INET, SOCK_STREAM)
c.connect((HOST,PORT))
c.send(NICKNAME.encode())
while True:
    #send the client info to the server
    
    # c.send(CLIENT_ID.encode())
    #Client input
    clientString = input("Enter Message:\n\n")
    if clientString.upper() == "DISCONNECT":
        c.close()
    #Send the client input to server
    c.send(clientString.encode())
    print("\n\n" + sString)
    #Read messages from Server
    sString = c.recv(1024)
    sString = sString.decode()
