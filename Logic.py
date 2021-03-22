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

def queueCreate(QueuesP, port):
    q = Queue(maxsize = 0)
    QueuesP[port] = q
    print("se creo la cola "+str(port))
    return "QC"

def queueList(QueuesP):
    listQ = ""
    for i in QueuesP:
        listQ += " -"+i+"\n"
    return listQ

def queueDelete(QueuesP, port):
    try:
        QueuesP.pop(port)
        print("se eliminó la cola "+str(port))
        return "QD"
    except:
        return "QE"

def queueMessage(QueuesP, port, message):
    try:
        QueuesP[port].put(message)
        print("se añadió el mensaje a la cola "+str(port))
        print("mensaje",message)
        return "MA"
    except:
        return "ME"

#Channels

def channelCreate(ChannelsP, port):
    ChannelsP[port] = []
    print("se creo el canal "+str(port))
    return "CC"

def channelList(ChannelsP):
    listC = ""
    for i in ChannelsP:
        listC += " -"+i+"\n"
    return listC

def channelDelete(ChannelsP, port):
    try:
        ChannelsP.pop(port)
        print("se eliminó el canal "+str(port))
        return "CD"
    except:
        return "CE"

def channelMessage(ChannelsP, ChannelsC, port, message):
    try:
        for i in ChannelsP[port]:
            ChannelsC[i].put(message)

        print("se añadió el mensaje a el canal "+str(port))
        print("mensaje",message)
        return "MA"
    except:
        return "ME"