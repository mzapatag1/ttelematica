# import socket programming library 
import socket 
import packet

# import thread module 
from _thread import *
import threading
import sys
import os

#commands:
#Bucket -> b = create, delete, list
#file -> f = download, load, list, delete

print_lock = threading.Lock() # thread function 

#method for different clients 
def threaded(c, Queues, port): 

    while True: 

        data = c.recv(1024) # command received from client
        if not data: 
            print('Bye')
            #print_lock.release() # lock released on exit 
            break
        else:
            Id, command, message = packet.unpack(str(data.decode("utf-8")))
            if Id == 'q':

                if command == "create":
                    response = packet.queueCreate(Queues, port)
                
                elif command == "list":
                    response = packet.queueList(Queues)
                
                elif command == "delete":
                    response = packet.queueDelete(Queues, port)
                
                elif command == "message":
                    response = packet.queueMessage(Queues, port, message)
                
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

    while True: 

        c, addr = s.accept() # establish connection with client 
        #print_lock.acquire() # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])
        identification = str(addr[0])+":"+str(addr[1])
        # Start a new thread
        try:
            start_new_thread(threaded, (c, Queues, identification)) 
        except:
            continue
    s.close() 


if __name__ == '__main__': 
    Main() 