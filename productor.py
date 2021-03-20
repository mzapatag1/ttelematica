# Import modules
import socket 
import json
import sys
import os
import time

#Commands
#   queue
#       q create
#       q list
#       q delete
#       q message

def Main(): 
    host = 'localhost' # local host IP '127.0.0.1'

    port = 8000 # Define the port on which you want to connect 

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    s.connect((host,port))  # connect to server on local computer 

    s.send(bytes("1", "utf-8"))
    while True: 
        # command to send to server 
        message = str(input()).strip()
        commands = message.split(' ')
        if message == 'exit':
                break
        elif len(commands)>=2:
            Id = commands[0].strip()
            command = commands[1].strip()
            #command about buckets
            if Id == 'q':
                #create a bucket
                if command == 'create':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)

                #list buckets
                elif command == 'list':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)

                #delete a bucket
                elif command == 'delete':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)
                
                elif command == 'message':
                    message = input("Ingresa el mensaje: ")
                    s.send(bytes(Id+" "+command+" "+message, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)
                else:
                    print("comando incorrecto")

            #commands about files
            elif Id == 'f':
                print("no implementado")
            else:
                print('there are only 2 options q or c')
        else:
            print('Invalid Command')

    # close the connection 
    s.close() 

if __name__ == '__main__': 
    Main() 