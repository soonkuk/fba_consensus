import pickle
import socket
import time
import uuid

class Packet():
    def __init__(self, node, ip, message_type, message=None): 
        self.node = node                # node = sender node name
        self.ip = ip                    # ip = sender ip                 
        self.type = message_type        # message type = 'ping' or scp message type(nomination, prepare, commit, client)
        self.data = message             # message = instance of Message()

def send(host, port, packet):
    sender_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    sender_sock.connect((host, port))
    sender_sock.send(pickle.dumps(packet))

def send2(host, port, packet):
    sender_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    sender_sock.connect((host, port))
    sender_sock.send(pickle.dumps(packet))

def broadcast(quorum_conf, packet):
    # receiver = list(filter(lambda x : x[1][1] == 'connect', quorum_conf['validators'].items()))
    for _, v in quorum_conf['validators'].items():
        send('localhost', v[0], packet)