#ChatServer.py

from socket import *
import string
import sys
import threading
from datetime import datetime

clients = [] #list for the client connections
client_names = {} #dict for the client names and ID


####################################################################

# broadcasts the message to all clients except the sender

####################################################################
def broadcast(c, str):
    broadcast_names = "Broadcasted: "
    for client, name in zip(clients, client_names):
            if c != client:
                client.send(str.encode())
                if(broadcast_names[-1] != " "):
                    broadcast_names += ","
                broadcast_names += name
    print(broadcast_names)

####################################################################

# gets the time from the message

####################################################################
def get_time_msg(cString):
    cTime = cString[cString.find("timestamp\": \"") + \
        len("timestamp\": \""):len(cString)-1]
    return cTime

####################################################################

# gets the nickname from the message

####################################################################
def get_name(cString):
    cName = cString[cString.find("type: \"nickname\", \"nickname\": \"") + \
        len("type: \"nickname\", \"nickname\": \""):\
            cString.find("\", \"clientID\": \"")]  
    return cName     

####################################################################

# gets the message from the client

####################################################################
def get_msg(cString):
    cMsg = cString[cString.find(", \"message\": \"") + len(", \"message\": \""):\
        cString.find("\", \"timestamp\": ")]
    return cMsg

####################################################################

# gets message type

####################################################################
def get_msg_type(cString):
    msg_type = cString[cString.find("type\": \"") + len("type\": \""):cString.find("\", \"nickname\"")]
    return msg_type

####################################################################

# gets client id

####################################################################
def get_id(cString):
    cID = cString[cString.find("\", \"clientID\": \"") + len("\", \"clientID\": \""):\
        cString.find("\",\"timestamp\": \"")]
    return cID

####################################################################

# initializes new clients

####################################################################
def new_client(c):
    cString = c.recv(1024)
    cString = cString.decode()

    cName = get_name(cString) #get the client nickname
    cID = get_id(cString) #get the client ID

    global client_names
    
    #if the name is already existing, send an error to the client
    #and then close the connection
    if cName in client_names.keys():
        errorMsg = "\"type\": \"error\", " +\
                "\"message\": \"Nickname already in use"
        c.send(errorMsg.encode())
        c.close()
        exit()
    if cID in client_names.values():
        errorMsg = "\"type\": \"error\", " +\
                "\"message\": \"ID already in use"
        c.send(errorMsg.encode())
        c.close()
        exit()

    #send an ok to the client if name doesn't exist and
    #add it to the list of names
    c.send("ok".encode())
    client_names.update({cName:cID})
    
    #get the time and print out that the user has connected to the server
    cTime = get_time_msg(cString)

    print(f"{cTime}::{cName}: connected.")
    run = True
    while run:
        cString = c.recv(1024)
        cString = cString.decode()

        cTime = get_time_msg(cString)
        cMsg = get_msg(cString)
        cType = get_msg_type(cString)

        #if the client types in "disconnect", their connection will be closed
        #otherwise keep sending the messages
        if(cType.upper() == "DISCONNECT"):
            print(f"{cTime}::{cName}: disconnected")
            run = False
            break
        elif(cType.upper() == "MESSAGE"):
            broadcast_msg = "\"type\": \"broadcast\", " +\
                    "\"nickname\": \"" + cName + "\", " +\
                        "\"message\": \"" + cMsg + "\", "+\
                            "\"timestamp\": \"" + cTime + "\""
            cIP, cPort = c.getsockname()
            print("\nReceived: IP:", cIP, ", Port:", cPort,\
                ", Client-Nickname:" ,cName , ", Client ID:" , cID,\
                    ", Date/Time:" , cTime +", Msg-Size:"\
                    , len(cMsg))
            broadcast(c, broadcast_msg)
    clients.remove(c)
    client_names.pop(cName)
    c.close()   

####################################################################

# main function

####################################################################
def main():
    global clients #list of clients

    try:
        args = sys.argv
        if len(args) != 2:
            print("Usage: python ChatServer.py PORT")
            exit()
        try:
            port = int(args[1])
        except:
            print("Port invalid, not a number")

        if port > 65536:
            print("Port Number larger than 65536")
            exit()
        if port < 10000 or port > 11000:
            print("Port number outside of range, must be 10000 < PORT < 11000")
            exit()

        try:
            port = int(args[1])
            s = socket(AF_INET, SOCK_STREAM)
            s.bind(('', port))
        except:
            print(f"ERR - cannot create ChatServer socket using port number {port}")
            exit()
        s.listen()

        print("ChatServer started with server IP:",gethostbyname(gethostname()),", port:", str(port),"...")

        while True:
            c, addr = s.accept()
            clients += [c]
            threading.Thread(target=new_client,args=(c,),daemon=True).start()
        s.close()

    except(KeyboardInterrupt):
        for client in clients:
            client.close()
            clients.remove(client)
        client_names.clear()
        s.close()
        exit()

if __name__ == '__main__':
    main()
