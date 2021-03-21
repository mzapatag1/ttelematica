import os
import sys
import shutil
import time

def pack(packet_id, message):
    return chr(packet_id) + message


def unpack(data):
    info = data.split(' ')
    if info[0] == 'CONNECT':
        return info[0], info[1], info[2], info[3]
    elif info[0] == 'PULL':
        return info[0], None, None, info[1]
    else:
        return 'Error', None, None, None


def get_token():
    return 'a'

def c_queue(dic_p, dic_c, idq, token):
    q = dic_p.get(idq)
    dic_c[token] = q
    return 'Conected with queue'

def p_queue(dic_c, token):
    q = dic_c[token]
    return q.get()

