# import socket programming library 
import socket 
import Logic
import LogicConsumer as lc

# import thread module 
from _thread import *
import threading
import sys
import os

import json

print_lock = threading.Lock() # thread function 

def threaded(c, port, QueuesP, QueuesC, ChannelsP, ChannelsC):
    
    while True:
        login = c.recv(1024) # 
        data = str(login.decode("utf-8"))
        info = data.split(' ')
        user = info[0]
        password = info[1]
        #user, password = Logic.unpack(str(login.decode("utf-8")))

        try:
            f = open("auth.json")
            auth = json.load(f)
            auth = auth[0]
            #autenticación
            if auth[user] == password:
                print(user, ' has logged in' )
                response = user
                c.send(response.encode("utf-8"))

                # identify user type: consumer or producer
                data = c.recv(1024)
                Id = str(data.decode("utf-8"))

                if Id == "1":
                    producer(c, user, QueuesP, ChannelsP, ChannelsC)
                    break
                if Id == "2":
                    consumer(c, user, QueuesP, QueuesC, ChannelsP, ChannelsC)
                    break
            else:
                response = "Failed login"
                c.send(response.encode("utf-8"))
        except:
            response = "ERROR! Cannot find, try again"
            print(response, sys.exc_info())
            c.send(response.encode("utf-8"))


        
#method for different producers
def producer(c, port, QueuesP, ChannelsP, ChannelsC):

    while True: 

        data = c.recv(1024)  # command received from client
        if not data: 
            print('Bye')
            #print_lock.release() # lock released on exit 
            break
        else:
            Id, command, message, indice = Logic.unpack(str(data.decode("utf-8")))
            if Id == 'QUEUE':

                if command == "CREATE":
                    response = Logic.queueCreate(QueuesP, port)
                
                elif command == "LIST":
                    response = Logic.queueList(QueuesP)
                
                elif command == "DELETE":
                    response = Logic.queueDelete(QueuesP, port, indice)
                
                elif command == "MESSAGE":
                    response = Logic.queueMessage(QueuesP, port, message, indice)
                
                c.sendall(response.encode("utf-8"))
                
            if Id == 'CHANNEL':

                if command == "CREATE":
                    response = Logic.channelCreate(ChannelsP, port)
                
                elif command == "LIST":
                    response = Logic.channelList(ChannelsP)
                
                elif command == "DELETE":
                    response = Logic.channelDelete(ChannelsP, port, indice)

                elif command == "MESSAGE":
                    response = Logic.channelMessage(ChannelsP, ChannelsC, port, message, indice)
                
                c.sendall(response.encode("utf-8"))

    # connection closed 
    c.close() 

def consumer(c, port, QueuesP, QueuesC, ChannelsP, ChannelsC):

    while True: 
        data = c.recv(1024) # command received from client
        if not data: 
            print('Disconected') 
            break

        else:
            command, mode, idq, idp = lc.unpack(str(data.decode("utf-8")))
            if command == 'CONNECT':
                if mode == 'QUEUE':
                    response = lc.c_queue(QueuesP, QueuesC, idq, idp, port)
                
                elif mode == 'CHANNEL':
                    response = lc.c_channel(ChannelsC, ChannelsP, idq, idp, port)
                
                else:
                    response = 'Invalid command: Choose queue or channel to connect'

                c.sendall(response.encode("utf-8"))

            elif command == 'PULL':
                if mode == 'QUEUE':
                    response = lc.p_queue(QueuesC, port)

                elif mode == 'CHANNEL':
                    response = lc.p_channel(ChannelsC, port)

                else:
                    response = 'Invalid command: Choose queue or channel to pull'

                c.sendall(response.encode("utf-8"))

            elif command == 'LIST':
                if mode == 'QUEUE':
                    response = Logic.queueList(QueuesP)

                elif mode == 'CHANNEL':
                    response = Logic.channelList(ChannelsP)

                else:
                    response = 'Invalid command: Choose queue or channel to list'
                
                c.sendall(response.encode("utf-8"))

            else:
                response = 'Invalid Command: Command no recognize'
                c.sendall(response.encode("utf-8"))
            
    # connection closed 
    c.close() 


def Main(): 
    #host = "0.0.0.0" 
    host = "localhost" 
    #server port
    #port = 8080
    port = 8000
    #socket created
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #socket into listening mode
    s.bind((host, port)) 
    print("socket binded to port", port)
    
    s.listen(5) 
    print("socket is listening") 

    #diccionario para identificar las colas de cada productor
    #la clave es la direccion ip del productor el valor es una cola(objeto cola)
    QueuesP = {}

    #diccionario para que cada consumidor sepa a que cola esta suscrita
    #la clave es la direccion ip del consumidor el valor es una cola(objeto cola)
    QueuesC = {}

    #diccionario para identificar los canales de cada productor
    #la clave la dirrecion ip del productor, su valor es un arreglo que contiene los id de los consumidores
    ChannelsP = {}

    #diccionario que relaciona un consumidor con su cola para recibo de mensajes por parte de un canal
    #la clave es la direccion ip del consumidor el valor es una cola(objeto cola)
    ChannelsC = {}

    while True: 

        c, addr = s.accept() # establish connection with client 
        #print_lock.acquire() # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])
        identification = str(addr[0])+":"+str(addr[1])
        # Start a new thread
        try:
            #hilo para que el servidor siempre permanezca escuchando las conexiones 
            start_new_thread(threaded, (c, identification, QueuesP, QueuesC, ChannelsP, ChannelsC))
        except:
            continue
    s.close() 


if __name__ == '__main__':
    Main() 
