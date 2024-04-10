#ChatClient.py

from socket import *
import string
import sys
import threading
from datetime import datetime

start_time = "" #time that the client started
end_time = "" #time that the client ended
msg_sent = 0 #num of messages client sent (only type message)
msg_rcv = 0 #num of messages client received
char_sent = 0 #total number of characters sent
char_rcv = 0 #total number of characters received
run = True #variable to determine when to stop the thread and close the client socke

#get the current time function
def getTime():
    now = datetime.now()
    return(now.strftime("%Y-%m-%d %H:%M:%S"))

#get the time from the message
def get_time_msg(cString):
    cTime = cString[cString.find("timestamp\": \"") + \
        len("timestamp\": \""):len(cString)-1]
    return cTime

#finds the name in the message
def get_name(cString):
    cName = cString[cString.find("\"nickname\": \"") + \
        len("\"nickname\": \""):\
            cString.find("\", \"message\": \"")]  
    return cName   

#finds the message in the client message 
def get_msg(cString):
    cMsg = cString[cString.find(", \"message\": \"") + len(", \"message\": \""):\
        cString.find("\", \"timestamp\": ")]
    return cMsg

#determines the message type from client
def get_msg_type(cString):
    msg_type = cString[cString.find("type\": \"") + len("type\": \""):cString.find("\", \"nickname\"")]
    return msg_type

#function to send the message from a thread, takes in socket, nickname, and client id
def send_msg(c,NICKNAME, CLIENT_ID):
    global end_time
    global msg_sent
    global char_sent
    global run

    userInput = input("Enter Message:\n\n")
    while run:

        #if user types disconnect, set run to false and then server will close connection
        nowString = getTime() #get the current timestamp
        if userInput.upper() == "DISCONNECT":
            clientString = "\"type\": \"disconnect\", " +\
            "\"nickname\": \"" + NICKNAME + "\", " +\
                "\"clientID\": \"" + str(CLIENT_ID) + "\", "+\
                    "\"timestamp\": \"" + nowString + "\""
            run = False
            end_time = getTime()
            c.send(clientString.encode())   
            break

        else: #if the input wasn't 'disconnect', then send the message normally
            clientString = "\"type\": \"message\", " +\
                "\"nickname\": \"" + NICKNAME + "\", " +\
                    "\"message\": \"" + userInput + "\", "+\
                        "\"timestamp\": \"" + nowString + "\""
            msg_sent += 1
            char_sent += len(userInput)

        #Send the client string to server
        c.send(clientString.encode())    
        userInput = input("\n")
    

def main():
    args = sys.argv
    if len(args) != 5:
        print("Usage: python ChatClient.py HOSTNAME PORT NICKNAME CLIENT_ID")
        exit()

    HOST = args[1] #hostname
    PORT = int(args[2]) #port num
    NICKNAME = args[3] #nickname
    CLIENT_ID = int(args[4]) #client id
    global start_time #time that the client started
    global end_time #time that the client ended
    global msg_sent #num of messages client sent (only type message)
    global msg_rcv #num of messages client received
    global char_sent #total number of characters sent
    global char_rcv #total number of characters received
    global run

    #try block to catch ctrl+c signal so that it can close the client and threads gracefully
    try:
        #Create the socket and connect
        c = socket(AF_INET, SOCK_STREAM)
        c.connect((HOST,PORT))
        nowString = getTime() #current time
        #successfully connected to server
        print("ChatClient started with server IP:",HOST,", port:",\
             str(PORT),", nickname:", NICKNAME, ", client ID:", str(CLIENT_ID), \
                ", Date\Time:", nowString, "\n")

        nowString = getTime() #get current timestamp
        start_time = nowString
        initialMsg = "type: \"nickname\", \"nickname\": \"" \
            + NICKNAME + "\", \"clientID\": \"" +\
                str(CLIENT_ID) + "\",\"timestamp\": \"" +\
                    nowString + "\""
        # print(initialMsg)
        c.send(initialMsg.encode())
        sString = c.recv(1024)
        sString = sString.decode()

        msg_type = get_msg_type(sString)

        #checks if the nickname is already in use, if so, server 
        #sends error message and client will print it then close connection
        if(msg_type.upper() == "ERROR"):
            print("\"type\": \"error\", ",\
                    "\"message\": \"Nickname already in use")
            c.close()
            exit()

        send_msg_thread = threading.Thread(target=send_msg,args=(c,NICKNAME, CLIENT_ID,),daemon=True)
        send_msg_thread.start()

        while run:
            sString = c.recv(1024)
            sString = sString.decode()
            if(sString):
                #get the message info from the server and print the message
                sName = get_name(sString)
                sTime = get_time_msg(sString)
                sMsg = get_msg(sString)
                sString = sTime + " :: " + sName + ": " + sMsg 
                msg_rcv += 1
                char_rcv += len(sMsg)
                print(sString)

        send_msg_thread.join()
        print(f"\nSummary: start: {start_time}, end: {end_time}, msg sent: {msg_sent}, msg rcv:{msg_rcv}, char sent: {char_sent}, char rcv: {char_rcv}")
        c.close()
        sys.exit(0)
    except(KeyboardInterrupt):
        c.close()
        sys.exit(0)

if __name__ == '__main__':
    main()