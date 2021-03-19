#packet.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import time


def pack(packet_id, message):
    return chr(packet_id) + message

#method to separate the message
def unpack(data):
    info = data.split(' ')
    return info[0], info[1]

def send(socket, output_data):
    try:
        socket.send(output_data)
    except TypeError:
        socket.send(bytes(output_data, "utf-8"))

def queueCreate(queue, port):
    queue[port] = []
    print("se creo la cola "+str(port))
    return 0

def queueList(queue):
    for i in queue:
        print(i)
    return 0

def queueDelete(queue, port):
    queue[port] = []
    print("se eliminó la cola "+str(port))
    return 0