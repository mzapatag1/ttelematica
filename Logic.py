#packet.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import time
from queue import Queue


def pack(packet_id, message):
    return chr(packet_id) + message

#method to separate the message
def unpack(data):
    info = data.split(' ')
    if len(info)==2:    
        return info[0], info[1], 0
    index = data.index("message")
    return info[0], info[1], data[index+8:]

def send(socket, output_data):
    try:
        socket.send(output_data)
    except TypeError:
        socket.send(bytes(output_data, "utf-8"))

def queueCreate(queue, port):
    q = Queue(maxsize = 0)
    queue[port] = q
    print("se creo la cola "+str(port))
    return "QC"

def queueList(queue):
    listQ = ""
    for i in queue:
        listQ += " -"+i+"\n"
    return listQ

def queueDelete(queue, port):
    queue.pop(port)
    print("se eliminó la cola "+str(port))
    return "QE"

def queueMessage(queue, port, message):
    queue[port].put(message)
    print("se añadió el mensaje a la cola "+str(port))
    print("mensaje",message)
    return "MA"