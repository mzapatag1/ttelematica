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

def threaded(c, Queues, QueuesC, port):
    data = c.recv(1024)
    Id = str(data.decode("utf-8"))
    if Id == "1":
        producer(c, Queues, port)
    if Id == "2":
        consumer(c, Queues, QueuesC)
        
#method for different producers
def producer(c, Queues, port): 

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
                    response = Logic.queueCreate(Queues, port)
                
                elif command == "list":
                    response = Logic.queueList(Queues)
                
                elif command == "delete":
                    response = Logic.queueDelete(Queues, port)
                
                elif command == "message":
                    response = Logic.queueMessage(Queues, port, message)
                
                c.sendall(response.encode("utf-8"))
                
            if Id == 'c':

                if command == "create":
                    print("aun no implementado")
                
                elif command == "list":
                    print("aun no implementado")
                
                elif command == "delete":
                    print("aun no implementado")

    # connection closed 
    c.close() 

def consumer(c, dic_p, dic_c):
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
    # a forever loop to connect with clients

    Queues = {}
    QueuesC = {}

    while True: 

        c, addr = s.accept() # establish connection with client 
        #print_lock.acquire() # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])
        identification = str(addr[0])+":"+str(addr[1])
        # Start a new thread
        try:
            start_new_thread(threaded, (c, Queues, QueuesC, identification))
        except:
            continue
    s.close() 


if __name__ == '__main__':
    Main() 
