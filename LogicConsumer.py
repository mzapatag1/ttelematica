import os
import sys
import shutil
import time
from queue import Queue

def pack(packet_id, message):
    return chr(packet_id) + message


def unpack(data):
    info = data.split(' ')
    if info[0] == 'CONNECT':
        return info[0], info[1], info[2]

    elif info[0] == 'PULL':
        return info[0], info[1], None

    else:
        return 'Error', None, None


def c_queue(QueuesP, QueuesC, idq, port):
    try:
        q = QueuesP.get(idq)
        QueuesC[port] = q
        return 'Conected with queue'
    except:
        return 'Invalid id queue'

def p_queue(QueuesC, port):
    try:
        q = QueuesC[port]
        return q.get()
    except:
        return 'Empty queue'

def c_channel(ChannelsC, ChannelsP, idq, port):
    try:
        if port in ChannelsC:   
            ChannelsP[idq].append(port)
        else:
            q = Queue(maxsize = 0)
            ChannelsC[port] = q
            ChannelsP[idq].append(port)

        return 'Conected with channel'

    except:
        return 'Invalid id channel'

def p_channel(ChannelsC, port):
    try:
        q = ChannelsC[port]
        return q.get()
    except:
        return 'Empty channel'

