# import socket programming library 
import socket 
import Logic
import LogicConsumer as lc

# import thread module 
from _thread import *
import threading
import sys
import os

print_lock = threading.Lock() # thread function 

def threaded(c, port, QueuesP, QueuesC, ChannelsP, ChannelsC):
    data = c.recv(1024)
    Id = str(data.decode("utf-8"))
    if Id == "1":
        producer(c, port, QueuesP, ChannelsP, ChannelsC)
    if Id == "2":
        consumer(c, port, QueuesP, QueuesC, ChannelsP, ChannelsC)
        
#method for different producers
def producer(c, port, QueuesP, ChannelsP, ChannelsC):

    while True: 

        data = c.recv(1024)  # command received from client
        if not data: 
            print('Bye')
            #print_lock.release() # lock released on exit 
            break
        else:
            Id, command, message = Logic.unpack(str(data.decode("utf-8")))
            if Id == 'q':

                if command == "create":
                    response = Logic.queueCreate(QueuesP, port)
                
                elif command == "list":
                    response = Logic.queueList(QueuesP)
                
                elif command == "delete":
                    response = Logic.queueDelete(QueuesP, port)
                
                elif command == "message":
                    response = Logic.queueMessage(QueuesP, port, message)
                
                c.sendall(response.encode("utf-8"))
                
            if Id == 'c':

                if command == "create":
                    response = Logic.channelCreate(ChannelsP, port)
                
                elif command == "list":
                    response = Logic.channelList(ChannelsP)
                
                elif command == "delete":
                    response = Logic.channelDelete(ChannelsP, port)

                elif command == "message":
                    response = Logic.channelMessage(ChannelsP, ChannelsC, port, message)
                
                c.sendall(response.encode("utf-8"))

    # connection closed 
    c.close() 

def consumer(c, port, dic_p, dic_c, ChannelsP, ChannelsC):
    response = lc.get_token() # Get token
    c.sendall(response.encode("utf-8")) # Send token

    while True: 
        data = c.recv(1024) # command received from client
        if not data: 
            print('Disconected') 
            break

        else:
            command, mode, idq, token = lc.unpack(str(data.decode("utf-8")))
            if command == 'CONNECT':
                if mode == 'QUEUE':
                    response = lc.c_queue(dic_p, dic_c, idq, token)

                c.sendall(response.encode("utf-8"))

            elif command == 'PULL':
                response = lc.p_queue(dic_c, token)
                c.sendall(response.encode("utf-8"))
                
            else:
                response = 'Invalid Command'
                c.sendall(response.encode("utf-8"))
            



    # connection closed 
    c.close() 


def Main(): 
    host = "localhost" 
    #server port
    port = 8000
    #socket created
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #socket into listening mode
    s.bind((host, port)) 
    print("socket binded to port", port)
    
    s.listen(5) 
    print("socket is listening") 

    #diccionario para identificar las colas de cada productor
    QueuesP = {}

    #diccionario para que cada consumidor sepa a que cola esta suscrita
    QueuesC = {}

    #diccionario para identificar los canales de cada productor
    ChannelsP = {}

    #diccionario para identificar los canales de cada productor
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
