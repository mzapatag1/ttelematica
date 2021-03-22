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
        return info[0], info[1], 0, 0
    elif "message" in data:
        index = data.index("message")
        return info[0], info[1], data[index+8:-1].strip(), info[-1]
    return info[0], info[1], 0, info[2]

def send(socket, output_data):
    try:
        socket.send(output_data)
    except TypeError:
        socket.send(bytes(output_data, "utf-8"))

def queueCreate(QueuesP, port):
    if port not in QueuesP:
        q = Queue(maxsize = 0)
        QueuesP[port] = [q]
        print("se creo la cola en "+str(port))
        return "QC"
    else:
        q = Queue(maxsize = 0)
        QueuesP[port].append(q)
        print("se añadio una nueva cola en "+str(port))
        return "QC"

def queueList(QueuesP):
    listQ = ""
    for i in QueuesP:
        cont = 0
        for j in QueuesP[i]:
            if not j == False:
                listQ += " -"+i+" "+str(cont)+"\n"
            cont+=1
    return listQ

def queueDelete(QueuesP, port, indice):
    try:
        indiceI = int(indice)
        QueuesP[port][indiceI] = False
        print("se eliminó la cola "+str(port)+" "+indice)
        return "QD"
    except:
        return "QE"

def queueMessage(QueuesP, port, message, indice):
    try:
        indiceI = int(indice)
        QueuesP[port][indiceI].put(message)
        print("se añadió el mensaje a la cola "+str(port)+" "+indice)
        print("mensaje",message)
        return "MA"
    except:
        return "ME"

#Channels

def channelCreate(ChannelsP, port):
    if port not in ChannelsP:
        ChannelsP[port] = [[]]
        print("se creo el canal "+str(port))
        return "CC"
    else:
        ChannelsP[port].append([])
        print("se añadio el canal a "+str(port))
        return "CC"

def channelList(ChannelsP):
    listC = ""
    for i in ChannelsP:
        cont = 0
        for j in ChannelsP[i]:
            if not j == False:
                listC += " -"+i+" "+str(cont)+"\n"
            cont+=1
    return listC

def channelDelete(ChannelsP, port, indice):
    try:
        indiceI = int(indice)
        ChannelsP[port][indiceI]=False
        print("se eliminó el canal "+str(port)+" "+indice)
        return "CD"
    except:
        return "CE"

def channelMessage(ChannelsP, ChannelsC, port, message, indice):
    try:
        indiceI = int(indice)
        for i in ChannelsP[port][indiceI]:
            ChannelsC[i].put(message)

        print("se añadió el mensaje a el canal "+str(port)+" "+indice)
        print("mensaje",message)
        return "MA"
    except:
        return "ME"