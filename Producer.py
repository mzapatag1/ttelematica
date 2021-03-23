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
#       q delete [# de la cola]
#       q message [# de la cola]

def Main(): 
    #host = '100.24.162.39' # local host IP '127.0.0.1'

    #port = 8080 # Define the port on which you want to connect 

    host = "localhost"  
    port = 8000

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

    s.connect((host,port))  # connect to server on local computer 
    print('Connected')

# Authentication
    while True: 
        print('Please enter your username and password')            
        login = str(input()).strip()
        s.send(bytes(login, "utf-8"))

        data = login.split(' ')
        user = data[0]
        password = data[1]

            # Receive MOM's reply and decode
        resp = s.recv(1024)
        resp = str(resp.decode("utf-8"))

        # Manejar errores
        if resp == user:
            print('Welcome',resp)
            s.send(bytes("1", "utf-8"))
            break
        else:
            print(resp)


    while True: 
        # command to send to server 
        message = str(input()).strip()
        commands = message.split(' ')
        if message == 'exit':
            print("Bye!")
            break
        elif len(commands)>=2:
            Id = commands[0].strip()
            command = commands[1].strip()
            
            if Id == 'QUEUE':
                #create
                if command == 'CREATE':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)

                #list
                elif command == 'LIST':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)

                #delete
                elif command == 'DELETE':
                    s.send(bytes(Id+" "+command+" "+commands[2], "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)
                
                elif command == 'MESSAGE':
                    message = input("Ingresa el mensaje: ")
                    s.send(bytes(Id+" "+command+" "+message+" "+commands[2], "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)
                else:
                    print("comando incorrecto")

            
            elif Id == 'CHANNEL':
                #create
                if command == 'CREATE':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)

                #list
                elif command == 'LIST':
                    s.send(bytes(Id+" "+command, "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)

                #delete
                elif command == 'DELETE':
                    s.send(bytes(Id+" "+command+" "+commands[2], "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)
                
                elif command == 'MESSAGE':
                    message = input("Ingresa el mensaje: ")
                    s.send(bytes(Id+" "+command+" "+message+" "+commands[2], "utf-8"))

                    response = s.recv(1024)
                    response = str(response.decode("utf-8"))
                    print(response)
                else:
                    print("Wrong command")

            else:
                print('there are only 2 options QUEUE or CHANNEL')

        else:
            print('Invalid Command')

    # close the connection 
    s.close() 

if __name__ == '__main__': 
    Main() 