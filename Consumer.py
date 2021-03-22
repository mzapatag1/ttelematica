# Import modules
import socket 
import json
import sys
import os
import time

def Main(): 
    host = 'localhost' # local host IP '127.0.0.1'
    port = 8000 # Define the port on which you want to connect 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.connect((host,port))  # connect to server on local computer
    
    print('connected')
    s.send(bytes("2", "utf-8"))

    while True: 
        message = str(input()).strip()
        commands = message.split(' ')

        if commands[0] == 'exit':
            break

        elif commands[0] == "CONNECT":
            if commands[1] == 'QUEUE':
                s.send(bytes(message, "utf-8")) 
                data = s.recv(1024) 
                print('Received from the server :',str(data.decode("utf-8")))
            
            elif commands[1] == 'CHANNEL':
                s.send(bytes(message, "utf-8")) 
                data = s.recv(1024) 
                print('Received from the server :',str(data.decode("utf-8")))
            

        elif commands[0] == "PULL":
            if commands[1] == 'QUEUE':
                s.send(bytes(message, "utf-8")) 
                data = s.recv(1024) 
                print('Received from the server :',str(data.decode("utf-8")))

            elif commands[1] == 'CHANNEL':
                s.send(bytes(message, "utf-8")) 
                data = s.recv(1024) 
                print('Received from the server :',str(data.decode("utf-8")))
        
        else:
            print('Invalid Command')

    # close the connection 
    s.close() 

if __name__ == '__main__': 
    Main() 