#ChatServer.py

from socket import *
import sys
from _thread import *

from datetime import datetime


clients = []
def send_msg(c, str):
    for client in clients:
            if c != client:
                client.send(str.encode())
                
def new_client(c):
    #receive client name
    cName = c.recv(1024)
    cName = cName.decode()

    # cID = c.recv(1024)
    # cID = cID.decode()

    # print(cID + "\n")

    #current date
    now = datetime.now()
    now_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print(now_string + " :: " + cName + ": connected.\n") #client connected
    while True:
        cString = c.recv(1024)
        cString= cString.decode()
        now_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sString = now_string + " :: " + cName + ": " + cString

        send_msg(c, sString)
    c.close()   
def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: python ChatServer.py HOSTNAME")
        exit()
        
    port = int(args[1])

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', port))
    s.listen()

    print("listening on port ", port, "...")

    while True:
        c, addr = s.accept()
        global clients
        clients += [c]
        start_new_thread(new_client,(c,))
    s.close()

if __name__ == '__main__':
    main()