# Import modules
import socket 
import json
import sys
import os
import time

def Main(): 
    #host = '100.24.162.39' # local host IP '127.0.0.1'
    #port = 8080
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
            s.send(bytes("2", "utf-8"))
            break
        else:
            print(resp)

    while True: 
        message = str(input()).strip()
        commands = message.split(' ')

        if commands[0] == 'exit':
            print("Bye!")
            break

        elif len(commands) == 4:
            if commands[0] == "CONNECT":
                if commands[1] == 'QUEUE':
                    s.send(bytes(message, "utf-8")) 
                    data = s.recv(1024) 
                    print('Received from the server :',str(data.decode("utf-8")))

                elif commands[1] == 'CHANNEL':
                    s.send(bytes(message, "utf-8")) 
                    data = s.recv(1024) 
                    print('Received from the server :',str(data.decode("utf-8")))

                else:
                    print('Invalid command: choose queue or channel to connect')

            else:
                    print('Invalid command: command not recognized')


        elif len(commands) == 2:
            if commands[0] == "PULL":
                if commands[1] == 'QUEUE':
                    s.send(bytes(message, "utf-8")) 
                    data = s.recv(1024) 
                    print('Received from the server :',str(data.decode("utf-8")))

                elif commands[1] == 'CHANNEL':
                    s.send(bytes(message, "utf-8")) 
                    data = s.recv(1024) 
                    print('Received from the server :',str(data.decode("utf-8")))

                else:
                    print('Invalid command: choose queue or channel to connect')
            
            elif commands[0] == "LIST":
                if commands[1] == 'QUEUE':
                    s.send(bytes(message, "utf-8")) 
                    data = s.recv(1024) 
                    print('Received from the server :',str(data.decode("utf-8")))

                elif commands[1] == 'CHANNEL':
                    s.send(bytes(message, "utf-8")) 
                    data = s.recv(1024) 
                    print('Received from the server :',str(data.decode("utf-8")))

                else:
                    print('Invalid command: choose queue or channel to list')

            else:
                print('Invalid command: command no recognize')
        else:
            print("Invalid command: command no recognize")

    # close the connection 
    s.close() 
    print('Disconnected')

if __name__ == '__main__': 
    Main() 